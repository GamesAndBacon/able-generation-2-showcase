![Able Generation 2.0 — Build richer abilities. See what you author.](images/cover.svg)

# Able · Generation 2.0

**Richer abilities. Clearer authoring. More control over every execution.**

A visual tour of our custom Able: collision shapes, multiple phases, reactive gameplay, persistent state, and weapon integration.

**[Open the full visual showcase →](https://gamesandbacon.github.io/able-generation-2-showcase/)**

Built on Able 3.96 for Unreal Engine 5.8. “Generation 2.0” names this project's evolution.

### Choose a chapter

| Build the move | Control the execution | Improve the framework |
| :--- | :--- | :--- |
| [01 · Collision Shapes](#collision-shapes) | [02 · Multiple timelines](#timelines) | [10 · Collision performance](#collision-performance) |
| [07 · Root motion](#root-motion) | [03 · Gameplay events](#gameplay-events) | [11 · Networking and APIs](#networking-apis) |
| [08 · Ability Editor](#ability-editor) | [04 · Ability State](#ability-state) | [12 · Weapon integrations](#weapon-integrations) |
| [09 · Bindings and presentation](#task-library) | [05 · Passives](#passives) · [06 · Input](#enhanced-input) | [Testing and upgrading](#the-foundation-underneath) |

**Browse the images. Open Look closer for the controls behind them.** On the website, click any image to enlarge it.

Each **Look closer** panel includes a compact code directory. File links open the private development repo at revision **`5d605e0`** (12 October 2026), so the line numbers stay fixed. Repository access is required to open the source.

---

<a name="collision-shapes"></a>

## 01 · Shape the attack

**Able Collision Engine — hitboxes that match the move.**

Build reusable Collision Shapes from presets, outlines, and repeated pieces. Preview the volume beside its graph, drag its dimensions into place, and expose them through typed Params.

![Cross Slash's construction graph, live shape preview and parameter controls.](images/ace-cross-slash.png)

*Cross Slash: build the arc, inspect the volume, adjust its dimensions.*

| Drag it into shape | Every input, one click away |
| :---: | :---: |
| ![Ground Slam's Arc Shape node selected: Outer Radius, Height, Angle and Location handles on the ring, its inputs in Details.](images/ace-shape-handles.png) | ![Cross Slash's Transform Hulls in Details: Transform traced to Make Transform, Rotation to Make Rotator, X (Roll) as the Tilt Param.](images/ace-node-details.png) |
| **Handles:** select a node, then drag its radius, height, angle or location. | **Details:** follow a wire back to the Param behind it. |

<details>
<summary><strong>Look closer: handles, Details, ranges and abilities</strong></summary>

| Generators draw what they make | Shapes inside abilities |
| :---: | :---: |
| ![Cross Slash's Generate Arc Points selected: its points drawn along the arc, with Radius, Angle and Center handles.](images/ace-generator-handles.png) | ![GrenadeExplosion's Collision Query: a Sphere Shape of radius 500 in the Ability Editor viewport, with its location gizmo.](images/ace-in-ability.png) |
| **Generate Arc Points:** points, with Radius, Angle and Center handles. | **GrenadeExplosion:** a Sphere Shape query, drawn and placed in the viewport. |

| Inspect the construction | Compose another move |
| :---: | :---: |
| ![Cross Slash preview with debug points and viewport parameter handles.](images/ace-preview.png) | ![Morning Star composed from a sphere and repeated cone spikes.](images/ace-morning-star.png) |
| **Cross Slash:** debug a node and drag its handles. | **Morning Star:** reuse and repeat smaller pieces. |

![Collision Query exposes Cross Slash's Radius, Thickness, Angle, Height and Tilt with separate binding controls.](images/shape-parameters.png)

*Bind one dimension without replacing the whole parameter struct.*

- **Handles:** a drag writes the value where it lives: the pin's own value, or the Param it's wired from. Each drag is one undo; values computed by other nodes aren't draggable.
- **Node Details:** a selected node's inputs edit as on the node. Inputs from Get Shape Params name their Param, "X (Roll) (Tilt Param)"; inputs from other nodes fold out into those nodes' inputs, up to four nodes back, with lists folded.
- **Ranges:** a Params member's Value Range clamps every build, so a random 0 can't reach Build Shape. The Preview names each clamp.
- **Presets:** Box, Sphere, Capsule, Segment, Cylinder, Cone, Vision Cone, Arc, Dome, Star, Prism and Path.
- **Construction:** Hull, Extrude and Revolve; concave outlines split into convex pieces. Polygon, Rectangle, Star and Arc generators supply outlines.
- **Composition:** Merge, Transform, Duplicate, Repeat, Mirror and nested Shapes. Blueprint and native C++ share the building blocks.
- **Inspection:** coloured hulls with the node that made each, points, dimensions, warnings, **D** to see one node's output, and a preview that rebuilds as you edit.
- **Integration:** Query, Sweep, Watch for Overlap and targeting; negative query shapes, automatic range and per-field bindings. Ordinary Blueprint queries support typed Params and async completion.

Async completion returns to the game thread. Worker-safe shapes can also build off-thread; raycasts retain line-trace behavior.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Preset volumes | [AblPresetShapes.cpp · L13](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblPresetShapes.cpp#L13 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblPresetShapes.cpp")<br><sub>ACE · Private/Shape</sub> |
| Hull, outline and composition nodes | [AblCustomShapeNodes.cpp · L46](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblCustomShapeNodes.cpp#L46 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblCustomShapeNodes.cpp")<br><sub>ACE · Private/Shape</sub> |
| Concave outline decomposition | [AblShapeBuildPolygons.cpp · L110](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Build/AblShapeBuildPolygons.cpp#L110 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Build/AblShapeBuildPolygons.cpp")<br><sub>ACE · Private/Build</sub> |
| Ability query integration and Params | [ablCollisionShapes.cpp · L11](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablCollisionShapes.cpp#L11 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablCollisionShapes.cpp")<br><sub>AbleCore · Private</sub> |
| Per-field value bindings | [ablMemberBindings.cpp · L91](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablMemberBindings.cpp#L91 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablMemberBindings.cpp")<br><sub>AbleCore · Private</sub> |
| Typed Blueprint query pins | [K2Node_AblShapeQuery.cpp · L217](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineGraph/Private/K2Node_AblShapeQuery.cpp#L217 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineGraph/Private/K2Node_AblShapeQuery.cpp")<br><sub>ACE Graph · Private</sub> |
| Viewport node handles | [AblShapeNodeHandles.cpp · L282](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Preview/AblShapeNodeHandles.cpp#L282 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Preview/AblShapeNodeHandles.cpp")<br><sub>ACE Editor · Private/Preview</sub> |
| Node Details, traced through wires | [AblShapeNodeDetails.cpp · L206](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Blueprint/AblShapeNodeDetails.cpp#L206 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Blueprint/AblShapeNodeDetails.cpp")<br><sub>ACE Editor · Private/Blueprint</sub> |
| Details for the selected node | [AblShapeNodeSelection.cpp · L36](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/ShapeEditor/AblShapeNodeSelection.cpp#L36 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/ShapeEditor/AblShapeNodeSelection.cpp")<br><sub>ACE Editor · Private/ShapeEditor</sub> |
| A value written where it lives | [AblShapePinValues.cpp · L213](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Preview/AblShapePinValues.cpp#L213 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Preview/AblShapePinValues.cpp")<br><sub>ACE Editor · Private/Preview</sub> |
| Generator handles | [AblGeneratorHandles.cpp · L7](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Preview/AblGeneratorHandles.cpp#L7 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Preview/AblGeneratorHandles.cpp")<br><sub>ACE Editor · Private/Preview</sub> |
| Params kept in range | [AblShapeParamsLimits.cpp · L67](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblShapeParamsLimits.cpp#L67 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblShapeParamsLimits.cpp")<br><sub>ACE · Private/Shape</sub> |
| Create Params Struct | [AblShapeEditorUtils.cpp · L84](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Blueprint/AblShapeEditorUtils.cpp#L84 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Blueprint/AblShapeEditorUtils.cpp")<br><sub>ACE Editor · Private/Blueprint</sub> |

</details>

---

<a name="timelines"></a>

## 02 · Give one ability several phases

**Wind up. Sustain. Recover. Keep one execution.**

Each timeline owns its tasks, playback, loops and exit routes. Phase transitions preserve the running context; alternate attacks can also own separate cooldowns and targeting.

![Wind Up, Sustained Attack and Recovery tabs show the routes between phases.](images/timeline-phases.png)

*The phase tabs show what runs next.*

<details>
<summary><strong>Look closer: held loops and independent attacks</strong></summary>

| Sustain until input ends | Give a phase its own attack settings |
| :---: | :---: |
| ![Sustained Attack loops and routes to Recovery when its input channel fails.](images/timeline-settings.png) | ![A timeline owns a three-second cooldown and Cross Slash targeting with automatic range.](images/timeline-targeting.png) |
| **Channel failure → Recovery.** | **Own cooldown, target requirement and shape.** |

- Bind playback, loop count and destinations; route completion and channel failure separately.
- Choose a starting phase, find one by name, or pick random/weighted destinations using shared random values.
- Targets, stacks and scratchpads survive transitions. Tasks end with **Branched**; activation checks and cooldowns are not repeated.
- Add, rename, duplicate, reorder or remove phases; stable identities retain their tasks. Dependencies stay within a timeline.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Phase settings and defaults | [ablAbilityTimeline.cpp · L11](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityTimeline.cpp#L11 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityTimeline.cpp")<br><sub>AbleCore · Private</sub> |
| Transition, retained context and task queues | [ablAbilityInstance.cpp · L1118](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityInstance.cpp#L1118 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityInstance.cpp")<br><sub>AbleCore · Private</sub> |
| Completion and channel-failure routes | [ablAbilityInstance.cpp · L343](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityInstance.cpp#L343 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityInstance.cpp")<br><sub>AbleCore · Private</sub> |
| Request a phase; random destinations below | [ablAbilityContext.cpp · L348](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityContext.cpp#L348 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityContext.cpp")<br><sub>AbleCore · Private</sub> |
| Per-phase targeting; cooldown keys below | [ablAbility.cpp · L587](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbility.cpp#L587 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbility.cpp")<br><sub>AbleCore · Private</sub> |
| Tabs, routes and phase actions | [SAbilityTimelineSelector.cpp · L135](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityTimelineSelector.cpp#L135 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityTimelineSelector.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |

</details>

---

<a name="gameplay-events"></a>

## 03 · React when gameplay happens

**Typed gameplay events — respond to a result, instead of guessing its timing.**

Tags declare payload types. Send and Get Payload expose those types in Blueprint; Listen tasks release response groups when a matching event arrives.

![Typed Send Gameplay Event and Get Gameplay Event Payload nodes expose Scalable Float members from the selected tag.](images/typed-event-nodes.png)

*An existing registry tag supplies the payload type. Split pins expose its members.*

<details>
<summary><strong>Look closer: the registry and repeated responses</strong></summary>

![The project's Gameplay Event Registry pairs tags with payload structs.](images/event-registry.png)

*Declare the tag and type once; author with typed pins.*

![Listen for Gameplay Event uses Repeat, Queue, eight queued responses and a two-second response watchdog.](images/event-response-settings.png)

*Listen repeatedly, queue accepted events, and bound how long a response may run.*

- **Publish:** Started, Completed, Interrupted, Manual and supported Result events. Damage, spawn, query and committed barrel-shot results carry captured outcomes.
- **Route:** Self, Instigator, Targets or a specified component; combine sources and Blueprint waits across components.
- **Respond:** Once/Repeat, Ignore While Busy/Queue, limits and overflow counts. Dependents use event-relative delay or timeline timing.
- **Isolate:** each response gets its own context and scratchpads; optionally target the event subject. Read captured payload and source metadata.
- **Bind and diagnose:** whole payloads or individual fields, child-tag type inheritance, bounded dispatch, dropped-event counters, trace and clean cancellation.

Gameplay events are **local**; they do not automatically replicate or activate abilities. Ability Callbacks remain separate.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Tag registry and inherited payload types | [ablGameplayEventRegistry.cpp · L21](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Events/ablGameplayEventRegistry.cpp#L21 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Events/ablGameplayEventRegistry.cpp")<br><sub>AbleCore · Private/Events</sub> |
| Routing, dispatch limits and tracing | [ablGameplayEventRouter.cpp · L69](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Events/ablGameplayEventRouter.cpp#L69 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Events/ablGameplayEventRouter.cpp")<br><sub>AbleCore · Private/Events</sub> |
| Listen windows, sources and cancellation | [ablListenEventTask.cpp · L48](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablListenEventTask.cpp#L48 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablListenEventTask.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Response queues and isolated execution | [ablEventExecution.cpp · L187](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Events/ablEventExecution.cpp#L187 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Events/ablEventExecution.cpp")<br><sub>AbleCore · Private/Events</sub> |
| Typed Send node | [K2Node_AblSendGameplayEvent.cpp · L39](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/Blueprint/K2Node_AblSendGameplayEvent.cpp#L39 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/Blueprint/K2Node_AblSendGameplayEvent.cpp")<br><sub>AbleEditor · Private/Blueprint</sub> |
| Typed Get Payload node | [K2Node_AblGetGameplayEventPayload.cpp · L33](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/Blueprint/K2Node_AblGetGameplayEventPayload.cpp#L33 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/Blueprint/K2Node_AblGetGameplayEventPayload.cpp")<br><sub>AbleEditor · Private/Blueprint</sub> |

</details>

---

<a name="ability-state"></a>

## 04 · Remember between activations

**Ability State — structured memory for each caster.**

Keep charges, combo progress or a previous target on the Ability Component. Typed Get/Set nodes expose the selected struct's members.

![Get Ability State reads Has Charged, Charges and Combo Step; Set Ability State writes a changed charge count.](images/ability-state-nodes.png)

*Read the caster's values, change one, and retain the others.*

<details>
<summary><strong>Look closer: defaults, sharing and replication</strong></summary>

![Ability State selects ST Ability Memory, initializes three charges and uses Server replication.](images/ability-state-settings.png)

*Choose the struct, starting values, sharing key and replication policy together.*

- **Lazy storage:** create on first use; **Use State** can disable storage for selected casters. **Has State** reports availability.
- **Shared memory:** related abilities share a **State Key**. Component **State Overrides** supply different defaults.
- **Typed updates:** Context inside an ability; Component + Ability elsewhere. **Leave Unchanged** preserves a member without a Set pin; read-only structs use whole-state replacement.
- **Lifecycle:** reset one key or all states; struct/member edits refresh nodes.
- **Replication:** Local per machine, or server-authoritative values sent to the owning client.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Lazy storage, overrides and reset APIs | [ablAbilityComponent.cpp · L488](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L488 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |
| Shared state keys and struct selection | [ablAbility.cpp · L82](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbility.cpp#L82 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbility.cpp")<br><sub>AbleCore · Private</sub> |
| Replication callbacks and typed Get/Set | [ablAbilityState.cpp · L11](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityState.cpp#L11 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityState.cpp")<br><sub>AbleCore · Private</sub> |
| Typed pins and Leave Unchanged | [K2Node_AblAbilityState.cpp · L428](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/Blueprint/K2Node_AblAbilityState.cpp#L428 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/Blueprint/K2Node_AblAbilityState.cpp")<br><sub>AbleEditor · Private/Blueprint</sub> |
| State defaults inspector | [AblAbilityStateDetails.cpp · L30](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/AblAbilityStateDetails.cpp#L30 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/AblAbilityStateDetails.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |

</details>

---

<a name="passives"></a>

## 05 · Keep each player's effects independent

**Passives per instigator — separate stacks, expiry and attribution.**

Two players can apply the same Burn to one enemy without sharing its lifetime. Query, change or cancel one instigator's application.

![Passive settings use Unique Per Instigator, five maximum stacks and duration refresh on new stacks.](images/passive-settings.png)

*One ability type. A separate passive instance for each instigator.*

<details>
<summary><strong>Look closer: inspect ownership and cancel selectively</strong></summary>

![Get Passive Instigators and Get Current Stack Count for Passive Ability expose per-instigator query controls.](images/passive-instigator-nodes.png)

*List the applying actors, then inspect a particular actor's stacks.*

![Cancel Ability uses Remove One and filters Only Passives From Self.](images/passive-cancellation.png)

*Remove your own application without clearing somebody else's.*

Stacks, duration, decay and cooldowns are independent. APIs accept an optional **Instigator**; Get Current Passive Abilities lists each ability type once. Replication carries separate instances and stack changes.

Temporary tags are reference-counted: one effect ending keeps `Status.Burning` while another still owns it. **Remove One** removes a stack from each affected instance.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Per-instigator activation and stacking | [ablAbilityComponent.cpp · L953](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L953 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |
| Stack queries; instigator listing below | [ablAbilityComponent.cpp · L1134](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L1134 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |
| Selective passive and stack cancellation | [ablCancelAbilityTask.cpp · L31](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablCancelAbilityTask.cpp#L31 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablCancelAbilityTask.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Temporary-tag reference counting | [ablAbilityComponent.cpp · L2662](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L2662 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |

</details>

---

<a name="enhanced-input"></a>

## 06 · Make input part of the move

**Enhanced Input — hold, release and branch with Input Actions.**

Use the activation's Context Input or select a Manual Input. Channel and branch readers listen to trigger callbacks for their execution window.

![Enhanced Input channel controls use Context Input, Started and While Input Is Active.](images/enhanced-input.png)

*Hold the channel; route to Recovery when input stops.*

<details>
<summary><strong>Look closer: input modes and listening windows</strong></summary>

- **On Input branches** remember a callback while other conditions become ready.
- **While Input Is Active** follows the action lifecycle; **Until Event Occurs** ends on the selected callback, commonly Completed for release.
- Choose **Started, Ongoing, Triggered, Completed or Canceled**. Bind the action/trigger; same-component Branch/Play Ability can inherit Context Input.
- Listeners belong to one execution and detach at the window's end, including input-component replacement and lost mappings.

Physical hold/release behavior comes from the game's Input Actions and mapping contexts.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Supported trigger events and active phases | [ablInputTypes.cpp · L10](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Input/ablInputTypes.cpp#L10 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Input/ablInputTypes.cpp")<br><sub>AbleCore · Private/Input</sub> |
| Trigger callbacks, active state and cleanup | [ablInputListener.cpp · L80](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Input/ablInputListener.cpp#L80 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Input/ablInputListener.cpp")<br><sub>AbleCore · Private/Input</sub> |
| Hold/release channel conditions | [ablChannelingConditions.cpp · L36](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Channeling/ablChannelingConditions.cpp#L36 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Channeling/ablChannelingConditions.cpp")<br><sub>AbleCore · Private/Channeling</sub> |
| Latched On Input branch conditions | [ablBranchCondition.cpp · L60](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablBranchCondition.cpp#L60 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablBranchCondition.cpp")<br><sub>AbleCore · Private/Tasks</sub> |

</details>

---

<a name="root-motion"></a>

## 07 · Author the movement

**Root-motion tasks — dashes, pulls, knockbacks and leaps.**

Four dedicated tasks use Character Movement sources. Bind values, shape motion with curves, and control how velocity finishes.

![Root Motion Radial Force displays its radius and origin gizmo in the viewport beside its settings.](images/root-motion-editor.png)

*Place the origin. Preview the radius. Author the push or pull.*

<details>
<summary><strong>Look closer: directional force, tracking and jumping</strong></summary>

![Constant Force exposes direction space, strength-over-time and finish-velocity controls.](images/root-motion-constant.png)

*Choose the direction space and strength curve for a dash.*

| Close the gap | Leave the ground |
| :---: | :---: |
| ![Move To exposes destination tracking, stop distance and path curves.](images/root-motion-move.png) | ![Jump exposes distance, height and Finish On Landed.](images/root-motion-jump.png) |
| **Move To:** track a destination and stop short. | **Jump:** shape the arc and finish on landing. |

| Task | Main controls |
| :--- | :--- |
| **Constant Force** | World/Actor/Control Rotation/Control Yaw direction, strength curve, gravity. |
| **Radial Force** | Push/pull, moving origin, radius, horizontal force, fixed direction, distance/time falloff. |
| **Move To** | Tracking, stop distance, acceptance radius, keep height, path offset/time curves. |
| **Jump** | Rotation space, distance, height, path/time curves, minimum landed time. |

All share additive/override behavior, priority, source naming, cleanup, finish velocity and temporary movement-mode controls. Duration follows play rate; Move To/Jump can finish early. Character Movement provides source replication, with server and owning-client application by default.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Shared application, finish velocity and cleanup | [ablRootMotionTasks.cpp · L93](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp#L93 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Constant Force source | [ablRootMotionTasks.cpp · L380](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp#L380 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Radial Force source | [ablRootMotionTasks.cpp · L441](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp#L441 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Move To source and destination tracking | [ablRootMotionTasks.cpp · L547](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp#L547 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Jump source and landing behavior | [ablRootMotionTasks.cpp · L661](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp#L661 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablRootMotionTasks.cpp")<br><sub>AbleCore · Private/Tasks</sub> |

</details>

---

<a name="ability-editor"></a>

## 08 · Read the ability at a glance

**Ability Editor — clearer tracks, phase routes and preview controls.**

Task groups separate presentation, collision, damage, movement and reactions. Search and collapse tracks to keep a larger ability readable.

![Animation, collision, damage, movement and gameplay-event tasks are separated into timeline groups.](images/task-groups.png)

*Follow each system's timing without losing the whole move.*

<details>
<summary><strong>Look closer: editing and preview improvements</strong></summary>

- **Organization:** named groups, drag reordering, moving tasks between groups and category grouping. Search task/category/group, including collapsed matches.
- **Navigation:** cursor-centred Alt + wheel zoom, Shift + wheel pan, draggable time/frame scrubbing and clearer task bars.
- **Spatial editing:** W/E moves/rotates labelled task gizmos; per-value visibility and one undo per drag. Custom task variables can declare relative space, socket and visibility.
- **Preview:** No Loop, Loop Ability, Loop Timeline, Timeline Once and Force Transition. Faster searchable actor/target pickers, Respawn, Add/Override Target and an initial-timeline new-asset workflow.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Groups, ordering and category organization | [ablAbilityEditor.cpp · L590](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/ablAbilityEditor.cpp#L590 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/ablAbilityEditor.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |
| Task search and track construction | [SAbilityTimeline.cpp · L283](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityTimeline.cpp#L283 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityTimeline.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |
| Group headers and drag/drop rows | [SAbilityTimelineRows.cpp · L274](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityTimelineRows.cpp#L274 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityTimelineRows.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |
| Cursor-centred zoom and panning | [ablAbilityEditor.cpp · L1685](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/ablAbilityEditor.cpp#L1685 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/ablAbilityEditor.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |
| Task gizmo transforms | [AblTaskGizmos.cpp · L219](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/AblTaskGizmos.cpp#L219 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/AblTaskGizmos.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |
| Preview loop modes | [ablAbilityEditor.cpp · L2445](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/ablAbilityEditor.cpp#L2445 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/ablAbilityEditor.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |

</details>

---

<a name="task-library"></a>

## 09 · Bind it. Spawn it. Present it.

**Richer task authoring — customize each use of the move.**

Spawn Actor exposes the chosen class's spawn variables with dynamic bindings. Animation and camera-shake controls make presentation easier to configure.

![Spawn Actor exposes the Throwable class's bindable Data, Time Cooked and Instigator spawn variables.](images/spawn-variables.png)

*The selected class supplies the fields. Bind values for this execution.*

<details>
<summary><strong>Look closer: animation, camera shake and task bindings</strong></summary>

| Author the playback | Share the impact |
| :---: | :---: |
| ![Play Animation groups playback, duration, speed and blending controls.](images/animation-controls.png) | ![Nearby camera shake exposes epicenter, radii and falloff controls.](images/nearby-shake.png) |
| **Animation:** explicit playback, timing and blending. | **Camera shake:** nearby players with spatial falloff. |

- **Spawn:** class-aware typed variables, defaults/bindings, deferred initialization, attachment and result events.
- **Animation:** playback mode, duration/speed policies, start position, looping, blending, end behavior and migration validation.
- **Shake:** target/nearby recipients, bindable epicenter/radii/falloff, and owned-instance cleanup.
- **Bindings:** broader dynamic values, identifiers and Create/View Binding controls. Effects, sound and ability playback receive supporting authoring/lifecycle improvements.

Smaller completion, cancellation, attachment, damage, turning and cleanup fixes are grouped here rather than listed task by task.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Class-aware spawn fields and deferred values | [ablSpawnActorTask.cpp · L354](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablSpawnActorTask.cpp#L354 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablSpawnActorTask.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Animation playback and lifecycle | [ablPlayAnimationTask.cpp · L91](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablPlayAnimationTask.cpp#L91 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablPlayAnimationTask.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Nearby camera shake and owned instances | [ablPlayCameraShakeTask.cpp · L46](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablPlayCameraShakeTask.cpp#L46 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/Tasks/ablPlayCameraShakeTask.cpp")<br><sub>AbleCore · Private/Tasks</sub> |
| Dynamic property binding registration | [ablAbility.cpp · L476](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbility.cpp#L476 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbility.cpp")<br><sub>AbleCore · Private</sub> |
| Create/View Binding editor controls | [SAbilityPropertyBinding.cpp · L200](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityPropertyBinding.cpp#L200 "plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/Private/AbilityEditor/SAbilityPropertyBinding.cpp")<br><sub>AbleEditor · Private/AbilityEditor</sub> |

</details>

---

<a name="collision-performance"></a>

## 10 · Make collision cheaper—and visible

**Native shape execution, caching and ACE Profiler.**

Supported shape graphs compile into native execution steps. Geometry reuse and tighter queries reduce repeated work; the profiler separates build and query costs by shape.

![ACE Profiler recording three Shape classes: the cost graph with a hover readout, the per-class table, and Worst frames below.](images/ace-profiler.png)

*A synthetic test workload: hover the graph to read every line; Worst frames takes the costliest apart.*

<details>
<summary><strong>Look closer: where the savings come from</strong></summary>

- **Native Build Shape:** supported math, Params, composition, Branch and Select avoid Blueprint VM dispatch. Unsupported graphs retain the VM with diagnostics.
- **Reuse:** bounded Params caches, shared hulls, cross-build caching and source-change invalidation.
- **Geometry:** faster outline merging, known-face checks and query-only builds; compatible touching pieces can merge on reuse.
- **Queries:** adaptive broadphase, tighter bounds rejection, less scene locking and sweep tests ordered to find earlier blocking hits.
- **Batches and visibility:** worker-thread batches, tunable thresholds, per-shape build/query recording and an engine-sphere comparison baseline.
- **Worst frames:** each class's queries and builds, the slowest of each, the Params that slowest build was for, the game frame's length and hull cache pruning.
- **Saved recordings:** the last five, as a CSV of every frame and a summary; **Recordings** reopens one in the graph.

Repository A/B measurements cover specific workloads, not a universal speedup. The production profiler is separate from the optional test plugin.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Native shape graph compilation | [AblShapeProgramCompiler.cpp · L94](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Program/AblShapeProgramCompiler.cpp#L94 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Program/AblShapeProgramCompiler.cpp")<br><sub>ACE Editor · Private/Program</sub> |
| Native execution steps | [AblShapeProgramRunner.cpp · L92](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Program/AblShapeProgramRunner.cpp#L92 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Program/AblShapeProgramRunner.cpp")<br><sub>ACE · Private/Program</sub> |
| Params cache and bounded reuse | [AblShapeParamsCache.cpp · L94](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblShapeParamsCache.cpp#L94 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Shape/AblShapeParamsCache.cpp")<br><sub>ACE · Private/Shape</sub> |
| Shared hull cache | [AblHullCache.cpp · L54](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Geometry/AblHullCache.cpp#L54 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Geometry/AblHullCache.cpp")<br><sub>ACE · Private/Geometry</sub> |
| Adaptive candidate broadphase | [AblShapeBroadphase.cpp · L19](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Query/AblShapeBroadphase.cpp#L19 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Query/AblShapeBroadphase.cpp")<br><sub>ACE · Private/Query</sub> |
| Batch queries and overlap/sweep dispatch | [AblCollisionShapeQuery.cpp · L282](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Query/AblCollisionShapeQuery.cpp#L282 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Query/AblCollisionShapeQuery.cpp")<br><sub>ACE · Private/Query</sub> |
| Per-shape cost recording | [AblCollisionProfiler.cpp · L202](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Profiling/AblCollisionProfiler.cpp#L202 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Profiling/AblCollisionProfiler.cpp")<br><sub>ACE · Private/Profiling</sub> |
| Profiler window and cost breakdown | [SAblCollisionProfiler.cpp · L80](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Profiler/SAblCollisionProfiler.cpp#L80 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Profiler/SAblCollisionProfiler.cpp")<br><sub>ACE Editor · Private/Profiler</sub> |

| Saved recordings and summaries | [AblProfilerRecordings.cpp · L128](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Profiling/AblProfilerRecordings.cpp#L128 "plugins/AbleCollisionEngine/Source/AbleCollisionEngine/Private/Profiling/AblProfilerRecordings.cpp")<br><sub>ACE · Private/Profiling</sub> |
| Worst frames panel | [SAblCollisionProfiler.cpp · L558](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Profiler/SAblCollisionProfiler.cpp#L558 "plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/Private/Profiler/SAblCollisionProfiler.cpp")<br><sub>ACE Editor · Private/Profiler</sub> |

</details>

---

<a name="networking-apis"></a>

## 11 · Start abilities. Follow the result.

**Simpler APIs and leaner replication underneath.**

Try Activate Ability creates the context and reports Activated/Failed in one node. Cooldown notifications and adjustments give UI and gameplay direct timer control.

![Try Activate Ability exposes Activated, Failed, the created Context and the start result.](images/try-activate-ability.png)

*Start the selected ability and handle the outcome directly.*

<details>
<summary><strong>Look closer: cooldown controls and networking changes</strong></summary>

![Change Cooldown and Get Ability Cooldown Remaining expose Timeline Index and Instigator controls.](images/cooldown-controls.png)

*Adjust a timer in seconds, or read one phase/instigator's remaining time.*

- **Activation:** optional instigator, input action, starting timeline and target location. Blueprint and AI can select an attack phase.
- **Cooldowns:** Started/Changed/Ended notifications, remaining seconds and single/all-timer adjustments.
- **Replication:** compact contexts omit implied/default values; project opt-in push model avoids unnecessary comparisons. State uses compact keys for owning-client replication; restarts use normal active-ability replication.
- **Shared choices:** per-visit random Int/Float values support corresponding timeline selections between machines.

Screenshots show the APIs, not network traffic. Gameplay-critical transitions still need server control. Remaining replication limits include same-timeline restarts, passive timeline changes and late-join shared randomness; gameplay events stay local.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Try Activate Ability | [ablAbilityComponent.cpp · L803](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L803 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |
| Cooldown adjustments and notifications | [ablAbilityComponent.cpp · L1771](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L1771 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |
| Compact context serialization | [ablAbilityContext.cpp · L532](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityContext.cpp#L532 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityContext.cpp")<br><sub>AbleCore · Private</sub> |
| Replication conditions and push-model opt-in | [ablAbilityComponent.cpp · L412](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp#L412 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityComponent.cpp")<br><sub>AbleCore · Private</sub> |
| Shared per-visit random values | [ablAbilityContext.cpp · L828](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityContext.cpp#L828 "plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/Private/ablAbilityContext.cpp")<br><sub>AbleCore · Private</sub> |

</details>

---

<a name="weapon-integrations"></a>

## 12 · Connect the weapon to the move

**EasyBallistics and bindable execution contexts.**

Fire Barrel and Barrel Command put weapon control on the timeline. Bind settings, aim at shot time, and publish committed-shot gameplay results.

![Fire Barrel exposes held-fire cleanup, barrel selection and bindable weapon configuration.](images/fire-barrel.png)

*Refresh configuration while firing; choose how it restores or stops.*

<details>
<summary><strong>Look closer: barrel commands and shot-time aiming</strong></summary>

| Control the weapon | Resolve the aim |
| :---: | :---: |
| ![Barrel Command lists firing, configuration, ammo, charge, chamber and spool operations.](images/barrel-commands.png) | ![Easy Aim in View Trace mode exposes view-source and obstruction settings.](images/easy-aim.png) |
| **Commands:** fire, stop, configure, reload and more. | **Easy Aim:** choose the source and handle obstructions. |

- Select barrels explicitly or through targets; bind configuration and refresh/restore policy.
- Command firing, ammo, charge, chamber unloading, fire mode, spooling and shooting blocking.
- Aim through View Trace, a world point, actor or component; configure view source, offsets and obstructions. Dynamic binding and barrel delegates remain available.
- Apply external stat overrides with **139 typed value getters**. Result events expose committed authority-side shot data and captured bullet references.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Fire Barrel lifecycle and shot results | [AblEBFireTask.cpp · L38](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleEasyBallistics/Source/AbleEasyBallistics/Private/Tasks/AblEBFireTask.cpp#L38 "plugins/AbleEasyBallistics/Source/AbleEasyBallistics/Private/Tasks/AblEBFireTask.cpp")<br><sub>Ballistics bridge · Private/Tasks</sub> |
| Barrel commands | [AblEBCommandTask.cpp · L9](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleEasyBallistics/Source/AbleEasyBallistics/Private/Tasks/AblEBCommandTask.cpp#L9 "plugins/AbleEasyBallistics/Source/AbleEasyBallistics/Private/Tasks/AblEBCommandTask.cpp")<br><sub>Ballistics bridge · Private/Tasks</sub> |
| Barrel selection and configuration | [AblEBTaskBase.cpp · L44](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleEasyBallistics/Source/AbleEasyBallistics/Private/Tasks/AblEBTaskBase.cpp#L44 "plugins/AbleEasyBallistics/Source/AbleEasyBallistics/Private/Tasks/AblEBTaskBase.cpp")<br><sub>Ballistics bridge · Private/Tasks</sub> |
| Shot-time Easy Aim resolution | [EBEasyAim.cpp · L8](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/EasyBalle55a27bc8c3fV25/Source/EasyBallistics/Private/Aiming/EBEasyAim.cpp#L8 "plugins/EasyBalle55a27bc8c3fV25/Source/EasyBallistics/Private/Aiming/EBEasyAim.cpp")<br><sub>EasyBallistics · Private/Aiming</sub> |
| Typed stat getters and overrides | [EBStatLibrary.h · L8](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/EasyBalle55a27bc8c3fV25/Source/EasyBallistics/Public/Stats/EBStatLibrary.h#L8 "plugins/EasyBalle55a27bc8c3fV25/Source/EasyBallistics/Public/Stats/EBStatLibrary.h")<br><sub>EasyBallistics · Public/Stats</sub> |

</details>

<details>
<summary><strong>Look closer: follow one execution's lifecycle</strong></summary>

![A bindable execution context supplies Bind Event to On Ability Timeline Changed and On Ability End.](images/context-lifecycle.png)

*Subscribe to the execution you started. Connect event handlers to react.*

Bindable contexts expose Start, End, Interrupt, Branch and Timeline Changed delegates. Typed factories and conversion support ordinary and pooled contexts; end cleanup removes forwarding/listeners before reuse. The integration is optional and local.

Both bridges existed in the repository's earliest snapshot; their later evolution is part of this generation.

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Context factories and conversion | [AbleContextBindableBlueprintLibrary.cpp · L5](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/ableContextBindable/Source/AbleContextBindable/Private/AbleContextBindableBlueprintLibrary.cpp#L5 "plugins/ableContextBindable/Source/AbleContextBindable/Private/AbleContextBindableBlueprintLibrary.cpp")<br><sub>Bindable contexts · Private</sub> |
| Delegate forwarding and disconnect | [AbleContextBindableContext.cpp · L51](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/ableContextBindable/Source/AbleContextBindable/Private/AbleContextBindableContext.cpp#L51 "plugins/ableContextBindable/Source/AbleContextBindable/Private/AbleContextBindableContext.cpp")<br><sub>Bindable contexts · Private</sub> |
| End cleanup before context reuse | [AbleContextBindableContext.cpp · L120](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/ableContextBindable/Source/AbleContextBindable/Private/AbleContextBindableContext.cpp#L120 "plugins/ableContextBindable/Source/AbleContextBindable/Private/AbleContextBindableContext.cpp")<br><sub>Bindable contexts · Private</sub> |

</details>

---

<a name="the-foundation-underneath"></a>

## The foundation underneath

**Optional test tooling. Clearer plugin boundaries. No compatibility code left.**

AbleTests groups editor automation, collision fixtures and reproducible measurements in a removable editor plugin. Production plugins do not depend on it.

![Able Tests is an optional plugin for automation, collision benchmarks, fixtures and reports, shown disabled.](images/able-tests-plugin.png)

*Available when needed; disabled in the captured editor session.*

<details>
<summary><strong>Look closer: modular plugins and upgrading</strong></summary>

![Plugin browser separates Able, Able Collision Engine, EasyBallistics, optional Able Tests and bindable contexts.](images/modular-plugins.png)

*The framework, collision engine and bridges have distinct responsibilities.*

Automation covers shape builds, query variants, batches, filters and lifecycle behavior. Reports record workloads, environment, seeds and latency distributions. The October review recorded **213 passing tests at that checkpoint**. On 12 October the Able and Collision Engine product suite ran **73 tests, all passing**, after the compatibility code was removed.

The project's own assets were converted once and saved in the current format; the conversions were then removed. Coming from the original Able, author these the current way:

| Original Able | Generation 2.0 |
| :--- | :--- |
| Ability-level playback | Timeline settings; Timeline 0 is the first phase. |
| Fixed collision volumes | Collision Shape with the matching ACE preset. |
| Arbitrary event payloads | Registered tag/type pairs and typed Send/Wait/Get nodes. |
| Key and action-name input | Input Actions, from the Context or picked by hand. |
| Animation checkboxes | Explicit playback, duration, speed and end policies. |
| Context named parameters | Ability State, or per-use dynamic bindings. |
| Get Cooldown / Get Max Stacks overrides | Cooldown and Max Stacks bindings. |

**Code directory** · [Source path key](#source-path-key)

| What to find | File · line |
| :--- | :--- |
| Optional module and measurement command | [AbleTestsModule.cpp · L13](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleTests/Source/AbleTests/Private/AbleTestsModule.cpp#L13 "plugins/AbleTests/Source/AbleTests/Private/AbleTestsModule.cpp")<br><sub>AbleTests · Private</sub> |
| Ability State coverage | [AblAbilityStateTests.cpp · L83](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleTests/Source/AbleTests/Private/Tests/AblAbilityStateTests.cpp#L83 "plugins/AbleTests/Source/AbleTests/Private/Tests/AblAbilityStateTests.cpp")<br><sub>AbleTests · Private/Tests</sub> |
| Serialization and push-model coverage | [AblNetworkContextTests.cpp · L68](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleTests/Source/AbleTests/Private/Tests/AblNetworkContextTests.cpp#L68 "plugins/AbleTests/Source/AbleTests/Private/Tests/AblNetworkContextTests.cpp")<br><sub>AbleTests · Private/Tests</sub> |
| Collision workloads and build measurements | [AblShapePerformanceTests.cpp · L30](https://github.com/GamesAndBacon/able-custom/blob/5d605e0d478f221d6108ef51bf053e94d538973b/plugins/AbleTests/Source/AbleTests/Private/Tests/AblShapePerformanceTests.cpp#L30 "plugins/AbleTests/Source/AbleTests/Private/Tests/AblShapePerformanceTests.cpp")<br><sub>AbleTests · Private/Tests</sub> |

</details>

<a name="capture-notes"></a>

<details>
<summary><strong>About these captures</strong></summary>

Captured directly from **shootcramental / Unreal Engine 5.8** on **11 October 2026**. Cross Slash, Morning Star and registry entries are existing assets. The Collision Engine's handles, node Details, Shape-in-ability and profiler captures were added on **12 October 2026** by AbleTests' capture tools, which open existing assets without saving them; the profiler records a synthetic test workload.

`AB_20_Showcase` and `ST_AbilityMemory` are temporary, unsaved authoring examples. Graphs and inspectors demonstrate controls, not validated gameplay implementations. Existing asset classes and registry entries were read without editing them.

Images are tightly framed screen captures; UI values/results were not painted into them. The cover is an original vector. The 12 October captures came from a fresh editor build; no benchmark or network validation was run for this document.


<a name="source-path-key"></a>

**Source path key**

File labels use the module keys below. Append the displayed folder and filename to find the file locally; hovering a file link also shows its full repository path.

| Module key | Repository folder |
| :--- | :--- |
| AbleCore | `plugins/AbleAbil334b52ee27f6V10/Source/AbleCore/` |
| AbleEditor | `plugins/AbleAbil334b52ee27f6V10/Source/AbleEditor/` |
| ACE | `plugins/AbleCollisionEngine/Source/AbleCollisionEngine/` |
| ACE Editor | `plugins/AbleCollisionEngine/Source/AbleCollisionEngineEditor/` |
| ACE Graph | `plugins/AbleCollisionEngine/Source/AbleCollisionEngineGraph/` |
| Ballistics bridge | `plugins/AbleEasyBallistics/Source/AbleEasyBallistics/` |
| EasyBallistics | `plugins/EasyBalle55a27bc8c3fV25/Source/EasyBallistics/` |
| Bindable contexts | `plugins/ableContextBindable/Source/AbleContextBindable/` |
| AbleTests | `plugins/AbleTests/Source/AbleTests/` |

Code entry points were moved to the revision above, and checked against it, on **12 October 2026**.

Markdown and the website share content and local images. This public repository contains only the showcase/media; plugin source and the Unreal project are maintained separately.

</details>
