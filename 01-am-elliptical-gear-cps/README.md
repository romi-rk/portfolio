# Elliptical Gear Set - Cyber-Physical Production Systems (Additive Manufacturing)

A parametric Lua script that generates a non-circular (elliptical) gear pair - axis of rotation at the ellipse's focus point, sine-wave tooth profile instead of a classical involute - and outputs print-ready geometry for a variable-speed-ratio gear drive. Built for the Cyber-Physical Production Systems using Additive Manufacturing case study at Deggendorf Institute of Technology.

`Lua` `Parametric CAD` `Additive Manufacturing` `Gear Design`

🎥 [Educational video (private, unlisted)](https://youtu.be/KgX8YWpbNac)

---

## What's in this repo

- **`EllipticalGearGenerator.lua`** - the script I wrote, parametric CAD code for the course's Lua-scriptable modeling tool. Not the full CAD project (materials, print profiles, slicer settings aren't included), just the generation logic.
- **`elliptical_gear_set.stl`** - the exported mesh the script produces, ready to slice and print.
- **`elevator-pitch.pdf`** - the team's hand-drawn pitch deck framing the problem (loud, jerky robotic-arm gear drives on a production line) and the product (a quieter, smoother-running elliptical gear set with a built-in variable transmission ratio).

## How the script works

Given just two inputs - center distance between shafts and the desired transmission ratio range (`i_max/i_min`) - the script derives the rest of the gear geometry:

1. **Ellipse geometry** - computes the ellipse's semi-major axis and eccentricity from the center distance and ratio range, then builds the reference pitch curve with the rotation axis at the focus (this is what gives the pair its continuously variable transmission ratio as they rotate, unlike a circular gear).
2. **Interference limits** - solves for the valid module/tooth-count/addendum range by checking the ellipse's minimum radius of curvature, so the generated teeth don't self-intersect at the tightest point of the ellipse.
3. **Sine tooth profile** - rather than an involute profile, the tooth flank follows a sine wave along the pitch curve. The script derives a "sine flank slope angle" (an analogue to pressure angle) and caps the addendum coefficient so the flank doesn't get too steep to print or mesh cleanly.
4. **Meshing** - places a second, mirrored gear at the specified center distance with the correct phase angle so the pair meshes correctly through a full rotation.
5. **Extrusion & output** - extrudes the 2D tooth profile to the specified face width and prints a design summary (module, tooth counts, min/max transmission ratio, flank angle) to the console for verification.

The repo includes only the final, revised version of the script - an earlier draft (fixed semi-major-axis/eccentricity inputs instead of center-distance/ratio-range, no interference validation) was superseded during development.

## Context

Group project (Group 30, 7 members, SS 2026). I wrote the parametric gear-generation script; teammates handled the print submission, the pitch deck, and the educational video presentation (linked above). Team member names appear in `elevator-pitch.pdf`.

## License / Use

Course project. Shared here for portfolio purposes.
