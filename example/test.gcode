
M73 P0 R1
M201 X1250 Y1250 Z400 E5000 ; sets maximum accelerations, mm/sec^2
M203 X180 Y180 Z12 E80 ; sets maximum feedrates, mm / sec
M204 P1250 R1250 T1250 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z2.00 E10.00 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec
M107
;TYPE:Custom
G90 ; use absolute coordinates
M83 ; extruder relative mode
M104 S170 ; set extruder temp for bed leveling
M140 S35 ; set bed temp
M109 R170 ; wait for bed leveling temp
M190 S35 ; wait for bed temp
G28 ; home all without mesh bed level
G29 ; mesh bed leveling 
M104 S202 ; set extruder temp
G92 E0.0
G1 Y-2.0 X179 F2400
G1 Z3 F720
M109 S202 ; wait for extruder temp

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
M204 S800
;TYPE:External perimeter
;WIDTH:0.419999
G1 F1637
G1 X97.19 Y82.81 E.45087
G1 X97.19 Y97.19 E.45087
M73 P25 R0
G1 X82.81 Y97.19 E.45087
M73 P26 R0
G1 X82.81 Y82.87 E.44899
M204 S1250
; stop printing object Shape-Box id:0 copy 0
M106 S84.15
;LAYER_CHANGE
;Z:0.4
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;0.4


G1 E-2.24 F4200
;WIPE_START
M73 P27 R0
G1 F8640
G1 X84.785 Y82.862 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z.4 F10800
;AFTER_LAYER_CHANGE
;0.4
; printing object Shape-Box id:0 copy 0
G1 Z.6
G1 X82.725 Y82.725
G1 Z.4
M73 P28 R0
G1 E3.2 F2400
M204 S800
;WIDTH:0.449999
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P29 R0
G1 X82.725 Y97.275 E.4925
M73 P30 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
M106 S170.85
;LAYER_CHANGE
;Z:0.6
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;0.6


M73 P31 R0
G1 E-2.24 F4200
;WIPE_START
M73 P32 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z.6 F10800
;AFTER_LAYER_CHANGE
;0.6
; printing object Shape-Box id:0 copy 0
G1 Z.8
G1 X82.725 Y82.725
G1 Z.6
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P33 R0
G1 X82.725 Y97.275 E.4925
M73 P34 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
M106 S255
;LAYER_CHANGE
;Z:0.8
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;0.8


M73 P35 R0
G1 E-2.24 F4200
;WIPE_START
M73 P37 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z.8 F10800
;AFTER_LAYER_CHANGE
;0.8
; printing object Shape-Box id:0 copy 0
G1 Z1
G1 X82.725 Y82.725
G1 Z.8
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P38 R0
G1 X82.725 Y97.275 E.4925
M73 P39 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:1
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;1


M73 P40 R0
G1 E-2.24 F4200
;WIPE_START
M73 P41 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z1 F10800
;AFTER_LAYER_CHANGE
;1
; printing object Shape-Box id:0 copy 0
G1 Z1.2
G1 X82.725 Y82.725
G1 Z1
M73 P42 R0
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P43 R0
G1 X82.725 Y97.275 E.4925
M73 P44 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:1.2
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;1.2


M73 P45 R0
G1 E-2.24 F4200
;WIPE_START
M73 P46 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z1.2 F10800
;AFTER_LAYER_CHANGE
;1.2
; printing object Shape-Box id:0 copy 0
G1 Z1.4
G1 X82.725 Y82.725
G1 Z1.2
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P47 R0
G1 X82.725 Y97.275 E.4925
M73 P48 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:1.4
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;1.4


M73 P50 R0
G1 E-2.24 F4200
;WIPE_START
M73 P51 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z1.4 F10800
;AFTER_LAYER_CHANGE
;1.4
; printing object Shape-Box id:0 copy 0
G1 Z1.6
G1 X82.725 Y82.725
G1 Z1.4
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P52 R0
G1 X82.725 Y97.275 E.4925
M73 P53 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:1.6
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;1.6


M73 P54 R0
G1 E-2.24 F4200
;WIPE_START
M73 P55 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z1.6 F10800
;AFTER_LAYER_CHANGE
;1.6
; printing object Shape-Box id:0 copy 0
G1 Z1.8
G1 X82.725 Y82.725
G1 Z1.6
M73 P56 R0
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P57 R0
G1 X82.725 Y97.275 E.4925
M73 P58 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:1.8
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;1.8


M73 P59 R0
G1 E-2.24 F4200
;WIPE_START
M73 P60 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z1.8 F10800
;AFTER_LAYER_CHANGE
;1.8
; printing object Shape-Box id:0 copy 0
G1 Z2
G1 X82.725 Y82.725
G1 Z1.8
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P61 R0
G1 X82.725 Y97.275 E.4925
M73 P62 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:2
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;2


M73 P64 R0
G1 E-2.24 F4200
;WIPE_START
M73 P65 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z2 F10800
;AFTER_LAYER_CHANGE
;2
; printing object Shape-Box id:0 copy 0
G1 Z2.2
G1 X82.725 Y82.725
G1 Z2
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P66 R0
G1 X82.725 Y97.275 E.4925
M73 P67 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:2.2
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;2.2


M73 P68 R0
G1 E-2.24 F4200
;WIPE_START
M73 P69 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z2.2 F10800
;AFTER_LAYER_CHANGE
;2.2
; printing object Shape-Box id:0 copy 0
G1 Z2.4
G1 X82.725 Y82.725
M73 P70 R0
G1 Z2.2
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P71 R0
G1 X82.725 Y97.275 E.4925
M73 P72 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:2.4
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;2.4


M73 P73 R0
G1 E-2.24 F4200
;WIPE_START
M73 P74 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z2.4 F10800
;AFTER_LAYER_CHANGE
;2.4
; printing object Shape-Box id:0 copy 0
G1 Z2.6
G1 X82.725 Y82.725
G1 Z2.4
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P75 R0
G1 X82.725 Y97.275 E.4925
M73 P77 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:2.6
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;2.6


M73 P78 R0
G1 E-2.24 F4200
;WIPE_START
M73 P79 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z2.6 F10800
;AFTER_LAYER_CHANGE
;2.6
; printing object Shape-Box id:0 copy 0
G1 Z2.8
G1 X82.725 Y82.725
G1 Z2.6
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P80 R0
G1 X82.725 Y97.275 E.4925
M73 P81 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:2.8
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;2.8


M73 P82 R0
G1 E-2.24 F4200
;WIPE_START
M73 P83 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z2.8 F10800
;AFTER_LAYER_CHANGE
;2.8
; printing object Shape-Box id:0 copy 0
G1 Z3
G1 X82.725 Y82.725
M73 P84 R0
G1 Z2.8
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P85 R0
G1 X82.725 Y97.275 E.4925
M73 P86 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
;LAYER_CHANGE
;Z:3
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;3


M73 P87 R0
G1 E-2.24 F4200
;WIPE_START
M73 P88 R0
G1 F8640
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z3 F10800
;AFTER_LAYER_CHANGE
;3
; printing object Shape-Box id:0 copy 0
G1 Z3.2
G1 X82.725 Y82.725
G1 Z3
G1 E3.2 F2400
M204 S800
G1 F1293
G1 X97.275 Y82.725 E.4925
G1 X97.275 Y97.275 E.4925
M73 P89 R0
G1 X82.725 Y97.275 E.4925
M73 P91 R0
G1 X82.725 Y82.785 E.49047
M204 S1250
; stop printing object Shape-Box id:0 copy 0
M73 P92 R0
G1 E-2.24 F4200
;WIPE_START
M73 P93 R0
G1 F8640;_WIPE
G1 X84.7 Y82.777 E-.912
;WIPE_END
G1 E-.048 F4200
G1 Z3.2 F10800
M107
;TYPE:Custom
; Filament-specific end gcode
G1 E-1 F2100 ; retract
G1 Z5 F720 ; Move print head up
G1 X178 Y178 F4200 ; park print head
G1 Z33 F720 ; Move print head further up
G4 ; wait
M104 S0 ; turn off temperature
M140 S0 ; turn off heatbed
M107 ; turn off fan
M221 S100 ; reset flow
M900 K0 ; reset LA
M84 ; disable motors
M73 P100 R0
; filament used [mm] = 29.35
; filament used [cm3] = 0.07
; filament used [g] = 0.09
; filament cost = 0.00
; total filament used [g] = 0.09
; total filament cost = 0.00
; estimated printing time (normal mode) = 1m 7s

; prusaslicer_config = begin
; avoid_crossing_perimeters = 1
; avoid_crossing_perimeters_max_detour = 0
; bed_custom_model = 
; bed_custom_texture = 
; bed_shape = 0x0,180x0,180x180,0x180
; bed_temperature = 35
; before_layer_gcode = ;BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]\n\n
; between_objects_gcode = 
; bottom_fill_pattern = monotonic
; bottom_solid_layers = 0
; bottom_solid_min_thickness = 0.5
; bridge_acceleration = 1000
; bridge_angle = 0
; bridge_fan_speed = 100
; bridge_flow_ratio = 0.95
; bridge_speed = 30
; brim_separation = 0
; brim_type = no_brim
; brim_width = 1
; clip_multipart_objects = 1
; color_change_gcode = M600
; compatible_printers_condition_cummulative = "printer_notes=~/.*PRINTER_VENDOR_PRUSA3D.*/ and printer_notes=~/.*PRINTER_MODEL_MINI.*/ and nozzle_diameter[0]==0.4";"nozzle_diameter[0]!=0.8 and ! (printer_notes=~/.*PRINTER_VENDOR_PRUSA3D.*/ and printer_notes=~/.*PRINTER_MODEL_MK(2.5|3).*/ and single_extruder_multi_material)"
; complete_objects = 1
; cooling = 1
; cooling_tube_length = 5
; cooling_tube_retraction = 91.5
; default_acceleration = 1250
; default_filament_profile = "Prusament PLA"
; default_print_profile = 0.15mm QUALITY @MINI
; deretract_speed = 40
; disable_fan_first_layers = 1
; dont_support_bridges = 1
; draft_shield = disabled
; duplicate_distance = 6
; elefant_foot_compensation = 0.1
; end_filament_gcode = "; Filament-specific end gcode"
; end_gcode = G1 E-1 F2100 ; retract\n{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+2, max_print_height)}{endif} F720 ; Move print head up\nG1 X178 Y178 F4200 ; park print head\n{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+30, max_print_height)}{endif} F720 ; Move print head further up\nG4 ; wait\nM104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\nM107 ; turn off fan\nM221 S100 ; reset flow\nM900 K0 ; reset LA\nM84 ; disable motors
; ensure_vertical_shell_thickness = 1
; external_perimeter_extrusion_width = 0.45
; external_perimeter_speed = 65
; external_perimeters_first = 0
; extra_loading_move = -2
; extra_perimeters = 1
; extruder_clearance_height = 20
; extruder_clearance_radius = 35
; extruder_colour = ""
; extruder_offset = 0x0
; extrusion_axis = E
; extrusion_multiplier = 1
; extrusion_width = 0.45
; fan_always_on = 1
; fan_below_layer_time = 100
; filament_colour = #272727
; filament_cooling_final_speed = 3.4
; filament_cooling_initial_speed = 2.2
; filament_cooling_moves = 4
; filament_cost = 16
; filament_density = 1.24
; filament_diameter = 1.75
; filament_load_time = 0
; filament_loading_speed = 28
; filament_loading_speed_start = 3
; filament_max_volumetric_speed = 15
; filament_minimal_purge_on_wipe_tower = 15
; filament_notes = ""
; filament_ramming_parameters = "120 100 6.6 6.8 7.2 7.6 7.9 8.2 8.7 9.4 9.9 10.0| 0.05 6.6 0.45 6.8 0.95 7.8 1.45 8.3 1.95 9.7 2.45 10 2.95 7.6 3.45 7.6 3.95 7.6 4.45 7.6 4.95 7.6"
; filament_settings_id = PLA
; filament_soluble = 0
; filament_spool_weight = 230
; filament_toolchange_delay = 0
; filament_type = PLA
; filament_unload_time = 0
; filament_unloading_speed = 90
; filament_unloading_speed_start = 100
; filament_vendor = Made for Prusa
; fill_angle = 45
; fill_density = 0%
; fill_pattern = triangles
; first_layer_acceleration = 800
; first_layer_acceleration_over_raft = 0
; first_layer_bed_temperature = 35
; first_layer_extrusion_width = 0.42
; first_layer_height = 0.2
; first_layer_speed = 35
; first_layer_speed_over_raft = 30
; first_layer_temperature = 202
; full_fan_speed_layer = 4
; fuzzy_skin = none
; fuzzy_skin_point_dist = 0.8
; fuzzy_skin_thickness = 0.3
; gap_fill_enabled = 1
; gap_fill_speed = 40
; gcode_comments = 0
; gcode_flavor = marlin
; gcode_label_objects = 1
; gcode_resolution = 0.0125
; gcode_substitutions = 
; high_current_on_filament_swap = 0
; host_type = octoprint
; infill_acceleration = 1000
; infill_anchor = 2.5
; infill_anchor_max = 12
; infill_every_layers = 1
; infill_extruder = 1
; infill_extrusion_width = 0.45
; infill_first = 0
; infill_only_where_needed = 0
; infill_overlap = 25%
; infill_speed = 140
; inherits_cummulative = "0.20mm SPEED @MINI";"Prusa PLA";"Original Prusa MINI & MINI+"
; interface_shells = 0
; ironing = 0
; ironing_flowrate = 15%
; ironing_spacing = 0.1
; ironing_speed = 15
; ironing_type = top
; layer_gcode = ;AFTER_LAYER_CHANGE\n;[layer_z]
; layer_height = 0.2
; machine_limits_usage = emit_to_gcode
; machine_max_acceleration_e = 5000
; machine_max_acceleration_extruding = 1250
; machine_max_acceleration_retracting = 1250
; machine_max_acceleration_travel = 1500,1250
; machine_max_acceleration_x = 1250
; machine_max_acceleration_y = 1250
; machine_max_acceleration_z = 400
; machine_max_feedrate_e = 80
; machine_max_feedrate_x = 180
; machine_max_feedrate_y = 180
; machine_max_feedrate_z = 12
; machine_max_jerk_e = 10
; machine_max_jerk_x = 8
; machine_max_jerk_y = 8
; machine_max_jerk_z = 2
; machine_min_extruding_rate = 0
; machine_min_travel_rate = 0
; max_fan_speed = 100
; max_layer_height = 0.25
; max_print_height = 180
; max_print_speed = 150
; max_volumetric_extrusion_rate_slope_negative = 0
; max_volumetric_extrusion_rate_slope_positive = 0
; max_volumetric_speed = 0
; min_bead_width = 85%
; min_fan_speed = 100
; min_feature_size = 25%
; min_layer_height = 0.07
; min_print_speed = 15
; min_skirt_length = 6
; mmu_segmented_region_max_width = 0
; notes = 
; nozzle_diameter = 0.4
; only_retract_when_crossing_perimeters = 0
; ooze_prevention = 0
; output_filename_format = {input_filename_base}_{layer_height}mm_{filament_type[0]}_{printer_model}_{print_time}.gcode
; overhangs = 1
; parking_pos_retraction = 92
; pause_print_gcode = M601
; perimeter_acceleration = 800
; perimeter_extruder = 1
; perimeter_extrusion_width = 0.45
; perimeter_generator = arachne
; perimeter_speed = 100
; perimeters = 1
; physical_printer_settings_id = 
; post_process = 
; print_settings_id = 0.20mm SPEED (custom)
; printer_model = MINI
; printer_notes = Don't remove the following keywords! These keywords are used in the "compatible printer" condition of the print and filament profiles to link the particular print and filament profiles to this printer profile.\nPRINTER_VENDOR_PRUSA3D\nPRINTER_MODEL_MINI\n
; printer_settings_id = Original Prusa MINI & MINI+ - CUSTOM
; printer_technology = FFF
; printer_variant = 0.4
; printer_vendor = 
; raft_contact_distance = 0.1
; raft_expansion = 1.5
; raft_first_layer_density = 90%
; raft_first_layer_expansion = 3
; raft_layers = 0
; remaining_times = 1
; resolution = 0
; retract_before_travel = 1.5
; retract_before_wipe = 70%
; retract_layer_change = 1
; retract_length = 3.2
; retract_length_toolchange = 4
; retract_lift = 0.2
; retract_lift_above = 0
; retract_lift_below = 179
; retract_restart_extra = 0
; retract_restart_extra_toolchange = 0
; retract_speed = 70
; seam_position = nearest
; silent_mode = 0
; single_extruder_multi_material = 0
; single_extruder_multi_material_priming = 1
; skirt_distance = 2
; skirt_height = 1
; skirts = 0
; slice_closing_radius = 0.049
; slicing_mode = regular
; slowdown_below_layer_time = 3
; small_perimeter_speed = 25
; solid_infill_below_area = 0
; solid_infill_every_layers = 0
; solid_infill_extruder = 1
; solid_infill_extrusion_width = 0.45
; solid_infill_speed = 140
; spiral_vase = 0
; standby_temperature_delta = -5
; start_filament_gcode = "M900 K{if printer_notes=~/.*PRINTER_MODEL_MINI.*/ and nozzle_diameter[0]==0.6}0.12{elsif printer_notes=~/.*PRINTER_MODEL_MINI.*/ and nozzle_diameter[0]==0.8}0.06{elsif printer_notes=~/.*PRINTER_MODEL_MINI.*/}0.2{elsif nozzle_diameter[0]==0.8}0.01{elsif nozzle_diameter[0]==0.6}0.04{else}0.05{endif} ; Filament gcode LA 1.5\n{if printer_notes=~/.*PRINTER_MODEL_MINI.*/};{elsif printer_notes=~/.*PRINTER_HAS_BOWDEN.*/}M900 K200{elsif nozzle_diameter[0]==0.6}M900 K18{elsif nozzle_diameter[0]==0.8};{else}M900 K30{endif} ; Filament gcode LA 1.0"
; start_gcode = G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM104 S170 ; set extruder temp for bed leveling\nM140 S[first_layer_bed_temperature] ; set bed temp\nM109 R170 ; wait for bed leveling temp\nM190 S[first_layer_bed_temperature] ; wait for bed temp\nG28 ; home all without mesh bed level\nG29 ; mesh bed leveling \nM104 S[first_layer_temperature] ; set extruder temp\nG92 E0.0\nG1 Y-2.0 X179 F2400\nG1 Z3 F720\nM109 S[first_layer_temperature] ; wait for extruder temp\n\n; intro line\nG1 X170 F1000\nG1 Z0.2 F720\nG1 X110.0 E8.0 F900\nG1 X40.0 E10.0 F700\nG92 E0.0\n\nM221 S95 ; set flow
; support_material = 1
; support_material_angle = 0
; support_material_auto = 0
; support_material_bottom_contact_distance = 0
; support_material_bottom_interface_layers = -1
; support_material_buildplate_only = 0
; support_material_closing_radius = 2
; support_material_contact_distance = 0.1
; support_material_enforce_layers = 0
; support_material_extruder = 0
; support_material_extrusion_width = 0.35
; support_material_interface_contact_loops = 0
; support_material_interface_extruder = 0
; support_material_interface_layers = 2
; support_material_interface_pattern = rectilinear
; support_material_interface_spacing = 0.2
; support_material_interface_speed = 80%
; support_material_pattern = rectilinear
; support_material_spacing = 2
; support_material_speed = 40
; support_material_style = grid
; support_material_synchronize_layers = 0
; support_material_threshold = 55
; support_material_with_sheath = 0
; support_material_xy_spacing = 1
; temperature = 202
; template_custom_gcode = 
; thick_bridges = 1
; thin_walls = 1
; threads = 8
; thumbnails = 16x16,220x124
; thumbnails_format = PNG
; toolchange_gcode = 
; top_fill_pattern = monotonic
; top_infill_extrusion_width = 0.4
; top_solid_infill_speed = 40
; top_solid_layers = 0
; top_solid_min_thickness = 0.7
; travel_speed = 180
; travel_speed_z = 0
; use_firmware_retraction = 0
; use_relative_e_distances = 1
; use_volumetric_e = 0
; variable_layer_height = 1
; wall_distribution_count = 1
; wall_transition_angle = 10
; wall_transition_filter_deviation = 25%
; wall_transition_length = 100%
; wipe = 1
; wipe_into_infill = 0
; wipe_into_objects = 0
; wipe_tower = 0
; wipe_tower_bridging = 10
; wipe_tower_brim_width = 2
; wipe_tower_no_sparse_layers = 0
; wipe_tower_rotation_angle = 0
; wipe_tower_width = 60
; wipe_tower_x = 170
; wipe_tower_y = 140
; wiping_volumes_extruders = 70,70
; wiping_volumes_matrix = 0
; xy_size_compensation = 0
; z_offset = 0
; prusaslicer_config = end
