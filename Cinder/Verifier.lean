import Lean

open Lean Elab Command

namespace Cinder

-- Capture the worker stream at import time, before command elaboration replaces
-- IO.getStdout with a buffered diagnostic stream.
initialize workerStdout : IO.FS.Stream ← IO.getStdout

-- These are policy restrictions in addition to the final kernel axiom audit.
-- In particular, candidates cannot execute their own elaborator or adjust options.
private def forbidden : List String := [
  "sorry", "admit", "sorryAx", "native_decide", "run_tac", "run_elab",
  "set_option", "macro", "elab", "syntax", "unsafe", "implemented_by",
  "axiom", "initialize", "builtin_initialize", "ofReduceBool", "ofReduceNat"
]

private def forbiddenName (name : String) : Bool :=
  (name.splitOn ".").any (fun component => forbidden.contains component)

private partial def checkSyntax (stx : Syntax) : CommandElabM Unit := do
  match stx with
  | .ident _ _ name _ =>
    if forbiddenName name.toString then
      throwError "CINDER_POLICY: forbidden identifier {name}"
  | .atom _ text =>
    if forbidden.contains text || text.startsWith "`" then
      throwError "CINDER_POLICY: forbidden syntax {text}"
  | .node _ _ args => args.forM checkSyntax
  | .missing => pure ()

-- Both strings name files inside the isolated worker. The statement file comes
-- from the problem registry; the candidate can supply only the proof file.
syntax (name := verify) "#cinder_verify " str str : command

elab "#cinder_context_ready" : command =>
  logInfo "CINDER_CONTEXT_READY"

@[command_elab verify] def elabVerify : CommandElab := fun stx => do
  if (← get).messages.hasErrors then
    throwError "CINDER_CONTEXT: trusted context has errors"
  let statementPath : TSyntax `str := ⟨stx[1]⟩
  let proofPath : TSyntax `str := ⟨stx[2]⟩
  let statement ← IO.FS.readFile statementPath.getString
  let env ← getEnv
  let target ← match Parser.runParserCategory env `term statement with
    | .ok target => pure (⟨target⟩ : TSyntax `term)
    | .error error => throwError "CINDER_STATEMENT: {error}"
  try
    liftTermElabM do
      let type ← Term.elabTermAndSynthesize target none
      unless ← Meta.isProp type do
        throwError "expected a proposition"
  catch ex =>
    throwError "CINDER_STATEMENT: {ex.toMessageData}"
  if (← get).messages.hasErrors then
    throwError "CINDER_STATEMENT: trusted statement has errors"
  -- Log messages are buffered until this command finishes. Emit and flush the
  -- phase boundary directly so it survives a fatal exit during candidate work.
  workerStdout.putStrLn (Json.mkObj [("cinder_event", toJson "candidate_ready")]).compress
  workerStdout.flush
  let proof ← IO.FS.readFile proofPath.getString
  let candidate ← match Parser.runParserCategory env `term proof with
    | .ok candidate => pure (⟨candidate⟩ : TSyntax `term)
    | .error error => throwError "CINDER_PARSE: {error}"
  checkSyntax candidate
  let name := mkIdent `cinder_verified_candidate
  let theoremName := (← getCurrNamespace) ++ name.getId
  let declaration ← `(theorem $name : $target := $candidate)
  elabCommand declaration
  -- Force completion of asynchronous kernel checking before reading axioms.
  let env ← getEnv
  if (← get).messages.hasErrors then
    throwError "CINDER_ELABORATION: candidate has errors"
  unless (env.toKernelEnv.find? theoremName).any (fun info => info matches .thmInfo _) do
    throwError "CINDER_INTERNAL: checked theorem missing"
  let axioms ← collectAxioms theoremName
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  let rejected := axioms.filter (fun ax => !allowed.contains ax)
  unless rejected.isEmpty do
    throwError "CINDER_AXIOMS: disallowed axioms {rejected}"
  let report := Json.mkObj [
    ("verdict", toJson "pass"),
    ("axioms", toJson (axioms.map Name.toString))
  ]
  logInfo m!"CINDER_RESULT:{report.compress}"

end Cinder
