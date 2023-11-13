M204 P1250 R1250 T1250 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X1.00 Y1.00 Z1.00 E1.00 ; sets the jerk limits, mm/sec
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
G28 ; home all without mesh bed level

G1 Z10 F720
G1 X50 Y50 F1800
G4 S1
; LAYER_CHANGE
G1 X100
G1 X75 Y100

G1 X50 Y50
G1 X100
G1 X75 Y100

G1 X50 Y50
G1 X100
G1 X75 Y100

G1 X50 Y50
G1 X100
G1 X75 Y100
; LAYER_CHANGE
G4 S3

M204 P20 R20 T20 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X1.00 Y1.00 Z1.00 E1.00 ; sets the jerk limits, mm/sec
; LAYER_CHANGE
G1 X50 Y50
G4 S1
G1 X100
G1 X75 Y100

G1 X50 Y50
G1 X100
G1 X75 Y100

G1 X50 Y50
G1 X100
G1 X75 Y100

G1 X50 Y50
G1 X100
G1 X75 Y100
; LAYER_CHANGE
G1 Z12