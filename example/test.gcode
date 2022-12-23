

; intro line
M73 P6 R1
G1 X170 F1000
M73 P7 R1
G1 Z0.2 F720
G1 X110.0 E8.0 F900
M73 P8 R1
G1 X40.0 E10.0 F700
G92 E0.0

M221 S95 ; set flow
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
M900 K0.2 ; Filament gcode LA 1.5
; ; Filament gcode LA 1.0
M107
;LAYER_CHANGE
;Z:0.2
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;0.2


M73 P14 R0
G1 E-3.2 F4200
M73 P23 R0
G1 Z.2 F10800
;AFTER_LAYER_CHANGE
;0.2
; printing object Shape-Box id:0 copy 0
G1 Z.4
G1 X82.81 Y82.81
G1 Z.2
M73 P24 R0
G1 E3.2 F2400
;M204 S800
;TYPE:External perimeter
;WIDTH:0.419999
G1 F1637
G1 X97.19 Y82.81 E.45087
G1 X97.19 Y97.19 E.45087
M73 P25 R0
G1 X82.81 Y97.19 E.45087
M73 P26 R0
G1 X82.81 Y82.87 E.44899