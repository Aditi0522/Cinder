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
      throwErrorAt stx "CINDER_POLICY: forbidden identifier {name}"
  | .atom _ text =>
    if forbidden.contains text || text.startsWith "`" then
      throwErrorAt stx "CINDER_POLICY: forbidden syntax {text}"
  | .node _ _ args => args.forM checkSyntax
  | .missing => pure ()

-- Parse one declaration structurally. Never elaborate model-provided commands,
-- attributes, names, auxiliary declarations, or declaration modifiers.
private def theoremParts (source : Syntax) : CommandElabM Syntax := do
  let source := if source.getKind == `lemma then
      source.setKind ``Parser.Command.declaration |>.modifyArg 1
        (fun d => d.setKind ``Parser.Command.theorem |>.setArg 0 (mkAtom "theorem"))
    else source
  unless source.getKind == ``Parser.Command.declaration &&
      source[1].getKind == ``Parser.Command.theorem do
    throwErrorAt source "CINDER_POLICY: expected one theorem; auxiliary declarations are unsupported"
  unless source[0].getArgs.all Syntax.isNone && source[1][1][1].isNone do
    throwErrorAt source "CINDER_POLICY: declaration modifiers, attributes and explicit universes are unsupported"
  let declaration := source[1]
  unless declaration[3].getKind == ``Parser.Command.declValSimple &&
      declaration[3][2].getArgs.all Syntax.isNone && declaration[3][3].isNone do
    throwErrorAt source "CINDER_POLICY: auxiliary where/termination declarations are unsupported; use local have/let"
  return source

private def signatureType (signature : Syntax) : TermElabM Expr := do
  Term.elabBinders signature[0].getArgs fun xs => do
    let type ← Term.elabTermAndSynthesize signature[1][1] none
    unless ← Meta.isProp type do
      throwError "expected a proposition"
    let type ← instantiateMVars (← Meta.mkForallFVars xs type)
    if type.hasMVar then
      throwError "unresolved metavariables in theorem signature"
    return type

-- All paths are supplied by the trusted Python driver.
syntax (name := verify) "#cinder_verify " str str str : command

elab "#cinder_context_ready" : command =>
  logInfo "CINDER_CONTEXT_READY"

@[command_elab verify] def elabVerify : CommandElab := fun stx => do
  if (← get).messages.hasErrors then
    throwError "CINDER_CONTEXT: trusted context has errors"
  let statementPath : TSyntax `str := ⟨stx[1]⟩
  let proofPath : TSyntax `str := ⟨stx[2]⟩
  let bindersPath : TSyntax `str := ⟨stx[3]⟩
  let statement ← IO.FS.readFile statementPath.getString
  let binders ← IO.FS.readFile bindersPath.getString
  let env ← getEnv
  let trustedSource := s!"theorem cinder_verified_candidate {binders} : {statement} := by sorry"
  let trusted ← match Parser.runParserCategory env `command trustedSource "statement.lean" with
    | .ok target => theoremParts target
    | .error error => throwError "CINDER_STATEMENT: {error}"
  let expected ← try
      liftTermElabM (signatureType trusted[1][2])
    catch ex => throwError "CINDER_STATEMENT: {ex.toMessageData}"
  if (← get).messages.hasErrors then
    throwError "CINDER_STATEMENT: trusted statement has errors"
  -- Log messages are buffered until this command finishes. Emit and flush the
  -- phase boundary directly so it survives a fatal exit during candidate work.
  workerStdout.putStrLn (Json.mkObj [("cinder_event", toJson "candidate_ready")]).compress
  workerStdout.flush
  let proof ← IO.FS.readFile proofPath.getString
  withReader (fun ctx => { ctx with fileName := "candidate.lean", fileMap := FileMap.ofString proof }) do
    try
      let parsed ← match Parser.runParserCategory env `term proof "candidate.lean" with
        | .ok term => pure (trusted.modifyArg 1 (fun d => d.modifyArg 3 (·.setArg 1 term)))
        | .error termError =>
          match Parser.runParserCategory env `command proof "candidate.lean" with
          | .ok declaration =>
            let declaration ← theoremParts declaration
            checkSyntax declaration[1][2]
            let actual ← liftTermElabM (signatureType declaration[1][2])
            unless ← liftTermElabM (Meta.isDefEq actual expected) do
              throwErrorAt declaration[1][2] "CINDER_SIGNATURE: candidate changes the trusted theorem signature"
            if (← get).messages.hasErrors then
              throwError "CINDER_SIGNATURE: candidate signature has errors"
            pure declaration
          | .error commandError =>
            let error := if proof.trim.startsWith "theorem " ||
                proof.trim.startsWith "lemma " then commandError else termError
            throwError "CINDER_PARSE: {error}; expected one proof term or theorem; auxiliary declarations are unsupported"
      let candidate := parsed[1][3][1]
      withRef candidate do
        checkSyntax candidate
        let name := mkIdent `cinder_verified_candidate
        let theoremName := (← getCurrNamespace) ++ name.getId
        let declaration := parsed.modifyArg 1 (fun d => d.modifyArg 1 (·.setArg 0 name))
        elabCommand declaration
        let env ← getEnv
        if (← get).messages.hasErrors then
          throwError "CINDER_ELABORATION: candidate has errors"
        let some (.thmInfo info) := env.toKernelEnv.find? theoremName |
          throwError "CINDER_INTERNAL: checked theorem missing"
        unless ← liftTermElabM (Meta.isDefEq info.type expected) do
          throwError "CINDER_SIGNATURE: checked theorem has a different type"
        let axioms ← collectAxioms theoremName
        let allowed := #[`propext, `Classical.choice, `Quot.sound]
        let rejected := axioms.filter (fun ax => !allowed.contains ax)
        unless rejected.isEmpty do
          throwError "CINDER_AXIOMS: disallowed axioms {rejected}"
        let report := Json.mkObj [
          ("verdict", toJson "pass"), ("axioms", toJson (axioms.map Name.toString))
        ]
        logInfo m!"CINDER_RESULT:{report.compress}"
    catch ex => logException ex

end Cinder
