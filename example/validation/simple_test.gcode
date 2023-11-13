M204 P4000 R1250 T4000 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X1.00 Y1.00 Z1.00 E1.00 ; sets the jerk limits, mm/sec
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
G28 ; home all without mesh bed level

G1 Z10 F720

;LAYER_CHANGE
G1 X90 Y70 F6000 ;A
;LAYER_CHANGE
G4 S1
;LAYER_CHANGE
G1 Y140 ;B
;LAYER_CHANGE
G4 S1
;LAYER_CHANGE
G1 X90 Y70 F6000 ;A
;LAYER_CHANGE
M204 P400 T400 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
G4 S1
;LAYER_CHANGE
G1 X90 Y70 F6000 ;A
;LAYER_CHANGE
G4 S1
;LAYER_CHANGE
G1 Y140 ;B
;LAYER_CHANGE
G4 S1
;LAYER_CHANGE
G1 X90 Y70 F6000 ;A
;LAYER_CHANGE
G4 S1
G1 X0 Y0
G28