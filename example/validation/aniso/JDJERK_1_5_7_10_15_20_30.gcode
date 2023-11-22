; TEST SERIES FOR VALIDATION OF JERK / JUNCTION DEVIATION
; use layer changing cue for timing

G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
G28 ; home all without mesh bed level

G1 Z10 F720 ; raise Nozzle



; ----- TESTING -----
; >>> SET VALUES <<<
M204 P50 R50 T50 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X1.00 Y1.00 Z1.00 E1.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----

; ----- TESTING -----
; >>> SET VALUES <<<
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X5.00 Y5.00 Z5.00 E5.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----

; ----- TESTING -----
; >>> SET VALUES <<<
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X7.00 Y7.00 Z7.00 E7.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----

; ----- TESTING -----
; >>> SET VALUES <<<
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X10.00 Y10.00 Z10.00 E10.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----

; ----- TESTING -----
; >>> SET VALUES <<<
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X15.00 Y15.00 Z15.00 E15.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----

; ----- TESTING -----
; >>> SET VALUES <<<
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X20.00 Y20.00 Z20.00 E20.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----

; ----- TESTING -----
; >>> SET VALUES <<<
G1 X50 Y50 F1800 ; starting position and travel speed
G4 S1 ; halt for 1s
M205 X30.00 Y30.00 Z30.00 E30.00 ; sets the jerk limits, mm/sec
G1 Z10.5
G1 Z10
; LAYER_CHANGE
; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 1

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 2

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 3

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 4

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 5

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 6

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 7

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 8

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 9

; CYCLE START
G1 X100
G1 X75 Y100
G1 X50 Y50
; CYCLE END 10
; LAYER_CHANGE
G1 Z10.5
G1 Z10
G4 S1 ; halt for 1 s
; ----- TESTING END -----
