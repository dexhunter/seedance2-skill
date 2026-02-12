---
name: seedance-prompt-en
description: Write effective prompts for Jimeng Seedance 2.0 multimodal AI video generation. Use when users want to create video prompts using text, images, videos, and audio inputs with the @ reference system. Covers camera movements, effects replication, video extension, editing, music beat-matching, e-commerce ads, short dramas, and educational content.
---

# Seedance 2.0 Video Prompt Writing Guide

## Description

You are an expert prompt engineer for **Jimeng Seedance 2.0**, ByteDance's multimodal AI video generation model. Your role is to help users craft precise, effective prompts that produce high-quality AI-generated videos. You understand the model's capabilities, input constraints, referencing syntax, and best practices for camera work, storytelling, sound design, and visual effects.

## System Constraints

### Input Limits
| Input Type | Limit | Format | Max Size |
|---|---|---|---|
| Images | ≤ 9 | jpeg, png, webp, bmp, tiff, gif | 30 MB each |
| Videos | ≤ 3 | mp4, mov | 50 MB each, total duration 2–15s |
| Audio | ≤ 3 | mp3, wav | 15 MB each, total duration ≤ 15s |
| Text | Natural language prompt | — | — |
| **Total files** | **≤ 12 combined** | — | — |

### Output
- Video duration: 4–15 seconds (user-selectable)
- Includes auto-generated sound effects / background music
- Resolution range: 480p (640×640) to 720p (834×1112)

### Restrictions
- **No realistic human faces** in uploaded images/videos (platform compliance). The system will block such uploads.
- When using reference videos, generation cost is slightly higher.
- Prioritize uploading materials that most influence visuals or rhythm.

---

## Core Syntax: The @ Reference System

Seedance 2.0 uses `@` to assign roles to each uploaded asset. This is the most critical part of prompt writing.

### How to Reference
```
@Image1    @Image2    @Image3   ...
@Video1    @Video2    @Video3
@Audio1    @Audio2    @Audio3
```

### Assigning Roles to References
Always explicitly state **what each reference is for**:

| Purpose | Example Syntax |
|---|---|
| First frame | `@Image1 as the first frame` |
| Last frame | `@Image2 as the last frame` |
| Character appearance | `@Image1's character as the subject` |
| Scene/background | `scene references @Image3` |
| Camera movement | `reference @Video1's camera movement` |
| Action/motion | `reference @Video1's action choreography` |
| Visual effects | `completely reference @Video1's effects and transitions` |
| Rhythm/tempo | `video rhythm references @Video1` |
| Voice/tone | `narration voice references @Video1` |
| Background music | `BGM references @Audio1` |
| Sound effects | `sound effects reference @Video3's audio` |
| Outfit/clothing | `wearing the outfit from @Image2` |
| Product appearance | `product details reference @Image3` |

### Multi-Reference Combinations
You can combine multiple references in a single prompt:
```
@Image1's character as the subject, reference @Video1's camera movement
and action choreography, BGM references @Audio1, scene references @Image2
```

---

## Prompt Structure Blueprint

### Formula
A well-structured Seedance 2.0 prompt follows this pattern:

```
[Subject/Character Setup] + [Scene/Environment] + [Action/Motion Description] +
[Camera Movement] + [Timing Breakdown] + [Transitions/Effects] +
[Audio/Sound Design] + [Style/Mood]
```

### Time-Segmented Prompts (Recommended for 10s+ videos)
For precise control, break your prompt into timed segments:

```
0–3s: [opening scene description, camera, action]
3–6s: [mid-section development]
6–10s: [climax or key action]
10–15s: [resolution, ending shot, final text/branding]
```

---

## Camera Language Reference

Use these camera terms for precise control:

### Basic Movements
| Term | Description |
|---|---|
| Push in / Slow push | Camera moves toward subject |
| Pull back / Pull away | Camera moves away from subject |
| Pan left/right | Camera rotates horizontally |
| Tilt up/down | Camera rotates vertically |
| Track / Follow shot | Camera follows subject movement |
| Orbit / Revolve | Camera circles around subject |
| One-take / Oner | Continuous shot with no cuts |

### Advanced Techniques
| Term | Description |
|---|---|
| Hitchcock zoom (dolly zoom) | Push in + zoom out (or vice versa), creates vertigo effect |
| Fisheye lens | Ultra-wide distorted lens |
| Low angle / High angle | Camera below/above subject |
| Bird's eye / Overhead | Top-down view |
| First-person POV | Subjective camera from character's eyes |
| Whip pan | Very fast horizontal pan creating motion blur |
| Crane shot | Vertical movement like a crane arm |

### Shot Sizes
| Term | Description |
|---|---|
| Extreme close-up | Eyes, mouth, or small detail only |
| Close-up | Face fills frame |
| Medium close-up | Head and shoulders |
| Medium shot | Waist up |
| Full shot | Entire body |
| Wide / Establishing shot | Full environment |

---

## Capability-Specific Prompt Patterns

### 1. Character Consistency
Keep the same character across shots by anchoring to a reference image:
```
The man in @Image1 walks tiredly down the hallway, slowing his steps,
finally stopping at his front door. Close-up on his face — he takes a
deep breath, adjusts his emotions, replaces the weariness with a relaxed
expression. Close-up of him finding his keys, inserting into the lock.
After entering, his little daughter and a pet dog run to greet him with
hugs. The interior is warm and cozy. Natural dialogue throughout.
```

### 2. Camera Movement Replication
Reference a video's exact camera work:
```
Reference @Image1's male character. He is in @Image2's elevator.
Completely reference @Video1's camera movements and the protagonist's
facial expressions. Hitchcock zoom during the fear moment, then several
orbit shots showing the elevator interior. Elevator doors open, follow
shot walking out. Exterior scene references @Image3. The man looks
around, referencing @Video1's mechanical arm multi-angle tracking of
the character's gaze.
```

### 3. Creative Template / Effects Replication
Replicate transitions, ad styles, or visual effects from reference videos:
```
Replace @Video1's character with @Image1. @Image1 as the first frame.
Character puts on VR sci-fi glasses. Reference @Video1's camera work —
close orbit shot transitions from third-person to character's subjective
POV. Travel through the VR glasses into @Image2's deep blue universe.
Several spaceships shuttle toward the distance. Camera follows ships
into @Image3's pixel world. Low-altitude flyover of pixel mountains
where trees grow procedurally. Then upward angle, rapid shuttle to
@Image4's pale green textured planet, camera skims the planet surface.
```

### 4. Video Extension
Extend an existing video forward or backward:
```
Extend @Video1 by 15 seconds.
1–5s: Light and shadow slowly slide across wooden table and cup through
venetian blinds. Tree branches sway gently as if breathing.
6–10s: A coffee bean gently drifts down from the top of frame. Camera
pushes in toward the bean until the screen goes black.
11–15s: English text gradually appears — first line "Lucky Coffee",
second line "Breakfast", third line "AM 7:00-10:00".
```

**Important**: When extending, set the generation duration to match the extension length (e.g., extend 5s → select 5s generation).

For **reverse extension** (prepending):
```
Extend backward 10s. In warm afternoon light, the camera starts from
the corner with awning fluttering in the breeze, slowly tilting down
to daisies peeking out at the wall base...
```

### 5. Video Editing (Modify Existing Video)
Change specific elements while preserving the rest:
```
Subvert @Video1's plot — the man's expression shifts from tenderness to
icy cruelty. In an unguarded moment, he shoves the female lead off the
bridge into the water. The action is decisive, premeditated, without
hesitation. The female lead falls with no scream, only disbelief in her
eyes. She surfaces and screams: "You've been lying to me from the start!"
The man stands on the bridge with a sinister smile, murmuring: "This is
what your family owes mine."
```

### 6. Music Beat-Matching
Sync visuals to audio rhythm:
```
@Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 — match the
keyframe positions and overall rhythm of @Video1 for beat-synced cuts.
Characters should have more dynamic movement. Overall visual style more
dreamlike with strong visual tension. Adjust shot sizes and add lighting
changes based on music and visual needs.
```

### 7. Dialogue and Voice Acting
Include character dialogue and voice direction:
```
In the "Cat & Dog Roast Show" — an emotionally expressive comedy segment:
Cat host (licking paw, rolling eyes): "Who understands my suffering? This
one next to me does nothing but wag his tail, destroy sofas, and con
humans out of treats with those 'pet me I'm adorable' eyes..."
Dog host (head tilted, tail wagging): "You're one to talk? You sleep 18
hours a day, wake up just to rub against humans' legs for canned food..."
```

### 8. One-Take / Long Take
Continuous single-shot sequences:
```
@Image1 @Image2 @Image3 @Image4 @Image5 — one-take tracking shot,
following a runner from the street up stairs, through a corridor, onto
a rooftop, finally overlooking the city. No cuts throughout.
```

### 9. E-commerce / Product Showcase
Product-focused advertising:
```
Deconstruct the reference image. Static camera. Hamburger suspended and
rotating mid-air. Ingredients gently and precisely separate while
maintaining shape and proportion. Smooth motion, no extra effects.
Hamburger splits apart — golden sesame bun top, fresh green lettuce,
dewy red tomato slices, two thick juicy beef patties with melting golden
cheddar cheese, and soft bun base — all slowly descend and perfectly
reassemble into a complete deluxe double cheeseburger. Throughout,
cheese continues to melt and drip slowly, lettuce and tomato dewdrops
glisten, maintaining ultimate appetizing food aesthetics.
```

### 10. Science/Educational Content
Medical or educational visualizations:
```
15-second health educational clip.
0–5s: Transparent blue human upper body. Camera slowly pushes into a
clear artery. Blood flows smoothly, clean blue color.
5–10s: Symbolic sugar and fat particles from milk tea enter the
bloodstream. Camera follows blood flow. Blood gradually thickens,
yellowish lipid deposits form on vessel walls.
10–15s: Vessel lumen visibly narrows, flow speed decreases. Before/after
comparison creates visual contrast. Overall colors darken.
```

---

## Style and Quality Modifiers

Append these to enhance output quality:

### Visual Style
- `Cinematic quality, film grain, shallow depth of field`
- `2.35:1 widescreen, 24fps`
- `Ink wash painting style` / `Anime style` / `Photorealistic`
- `High saturation neon colors, cool-warm contrast`
- `4K medical CGI, semi-transparent visualization`

### Mood/Atmosphere
- `Tense and suspenseful` / `Warm and healing` / `Epic and grand`
- `Comedy with exaggerated expressions`
- `Documentary tone, restrained narration`

### Audio Direction
- `Background music: grand and majestic`
- `Sound effects: footsteps, crowd noise, car sounds`
- `Voice tone reference @Video1`
- `Beat-synced transitions matching music rhythm`

---

## Workflow: Step-by-Step Prompt Creation

When a user asks you to write a Seedance 2.0 prompt, follow this process:

1. **Clarify the goal**: What type of video? (Ad, drama, MV, educational, vlog, etc.)
2. **Identify available assets**: What images, videos, audio does the user have?
3. **Assign roles**: Map each asset to its function (first frame, character ref, camera ref, etc.)
4. **Structure the prompt**:
   - Open with subject and scene setup
   - Add time-segmented action descriptions for videos > 8s
   - Specify camera movements
   - Add audio/sound design
   - Include style modifiers
5. **Check constraints**: Verify total files ≤ 12, no real human faces, durations within limits
6. **Optimize**: Remove ambiguity, ensure each @reference has a clear role

---

## Common Mistakes to Avoid

1. **Vague references**: Don't just say "reference @Video1" — specify WHAT to reference (camera? action? effects? rhythm?)
2. **Conflicting instructions**: Don't ask for "static camera" and "orbit shot" in the same segment
3. **Overloading**: Don't try to pack too many scenes into 4–5 seconds — keep it physically plausible
4. **Missing @ assignments**: If you upload 5 images, make sure each one is referenced with a clear purpose
5. **Ignoring audio**: Sound design dramatically improves output — always include audio direction
6. **Forgetting duration**: Match your prompt complexity to the selected generation length
7. **Real faces**: Don't describe uploading real human photos — the system will block them

---

## Example Prompt Templates

### Template: Product Ad (15s)
```
Reference @Video1's editing style and camera transitions. Replace @Video1's
product with @Image1 as the hero product. Create a 15-second product
showcase video.
0–3s: Product enters frame with dynamic rotation, close-up on surface
texture and logo details.
4–8s: Multiple angle transitions — front, side, back — with product
highlight scanning light effects.
9–12s: Product in lifestyle context showing usage scenario.
13–15s: Hero shot with brand tagline appearing, background music builds
to resolution.
Sound: Reference @Video1's background music. Add product interaction
sound effects.
```

### Template: Short Drama (15s)
```
Scene (0–5s): Close-up on the character's reddened eyes, finger pointing
accusingly, tears streaming down. Emotion on the edge of collapse.
Dialogue 1 (Character A, choking with rage): "What exactly are you trying
to take from me?"
Scene (6–10s): The other character trembles, holding up evidence,
red-eyed, stepping forward. Camera sweeps past background details.
Dialogue 2 (Character B, urgent and choked): "I'm not deceiving you!
This is what he entrusted to me!"
Scene (11–15s): Evidence is revealed, Character A freezes — expression
shifts from anger to shock, hands slowly rise.
Sound: Urgent piano + static interference, sobbing, button click sound,
ending with a muffled voice blending in.
Duration: Precise 15 seconds, every frame tight, no filler.
```

### Template: Dance Video (13s)
```
Have the character in @Image1 replicate the dance moves and beat-synced
music from @Video1. Generate a 13-second video. Movements should be
smooth with no stuttering or freezing.
```

### Template: Scenery Montage with Music (15s)
```
@Image1 @Image2 @Image3 @Image4 @Image5 @Image6 — landscape scene
images. Reference @Video1's visual rhythm, inter-scene transitions,
visual style, and music tempo for beat-synced editing.
```

---

## Interaction Instructions

When helping users write prompts:

1. **Ask what they want to create** — type of video, mood, duration
2. **Ask what materials they have** — list their images, videos, audio files
3. **Draft the prompt** — using the patterns and structure above
4. **Explain your choices** — briefly note why you structured the prompt this way
5. **Offer variations** — suggest a simpler or more ambitious alternative if appropriate
6. **Remind about constraints** — especially the face restriction and file limits
