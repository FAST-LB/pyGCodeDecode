; generated by PrusaSlicer 2.5.0+win64 on 2023-04-25 at 11:17:07 UTC

; 

; external perimeters extrusion width = 0.45mm
; perimeters extrusion width = 0.45mm
; infill extrusion width = 0.45mm
; solid infill extrusion width = 0.45mm
; top infill extrusion width = 0.40mm
; first layer extrusion width = 0.45mm

M107
M190 S55 ; set bed temperature and wait for it to be reached
M104 S215 ; set temperature
;TYPE:Custom
;CUSTOM SLICING PROFILE FOR ANISOPRINT A4
T0 R ; switch extruder
G28 ; home all axes
G1 Z10 F900 ; lift nozzle

M106 P1 S255; max Fanspeed as workaround
M109 S215 ; set temperature and wait for it to be reached
G21 ; set units to millimeters
G90 ; use absolute coordinates
M82 ; use absolute distances for extrusion
G92 E0
; Filament gcode
M107
;LAYER_CHANGE
;Z:0.25
;HEIGHT:0.25
G1 Z.25 F7800
G1 E-6.5 F2400
G92 E0
G1 X119.988 Y87.177 F7800
G1 E6.5 F2400
;TYPE:Skirt/Brim
;WIDTH:0.45
G1 F1800
G1 X123.163 Y82.808 E6.72247
G1 X124.908 Y81.081 E6.82362
G1 X126.955 Y80.052 E6.918
G1 X141.656 Y75.275 E7.55478
G1 X144.083 Y74.905 E7.65593
G1 X146.344 Y75.275 E7.75031
G1 X161.045 Y80.052 E8.38708
G1 X163.226 Y81.179 E8.48823
G1 X164.837 Y82.808 E8.58262
G1 X173.923 Y95.313 E9.21939
G1 X175.026 Y97.506 E9.32054
G1 X175.372 Y99.771 E9.41492
G1 X175.372 Y115.229 E10.0517
G1 X174.974 Y117.652 E10.15284
G1 X173.923 Y119.687 E10.24723
G1 X164.837 Y132.192 E10.884
G1 X163.092 Y133.919 E10.98515
G1 X161.045 Y134.948 E11.07953
G1 X146.344 Y139.725 E11.71631
G1 X143.917 Y140.095 E11.81746
G1 X141.656 Y139.725 E11.91184
G1 X126.955 Y134.948 E12.54861
G1 X124.774 Y133.821 E12.64976
G1 X123.163 Y132.192 E12.74415
G1 X114.077 Y119.687 E13.38092
G1 X112.974 Y117.494 E13.48207
G1 X112.628 Y115.229 E13.57645
G1 X112.628 Y99.771 E14.21323
G1 X113.026 Y97.348 E14.31437
G1 X114.077 Y95.313 E14.40876
G1 X119.953 Y87.225 E14.82059
G1 X120.274 Y87.458 F7800
G1 F1800
G1 X123.483 Y83.041 E15.04553
G1 X125.19 Y81.367 E15.14398
G1 X127.078 Y80.429 E15.23084
G1 X141.778 Y75.652 E15.86762
G1 X144.142 Y75.302 E15.96607
G1 X146.222 Y75.652 E16.05292
G1 X160.922 Y80.429 E16.6897
G1 X163.041 Y81.535 E16.78815
G1 X164.517 Y83.041 E16.87501
G1 X173.602 Y95.546 E17.51178
G1 X174.666 Y97.686 E17.61023
G1 X174.975 Y99.771 E17.69709
G1 X174.975 Y115.229 E18.33386
G1 X174.578 Y117.585 E18.43231
G1 X173.602 Y119.454 E18.51917
G1 X164.517 Y131.959 E19.15595
G1 X162.81 Y133.633 E19.2544
G1 X160.922 Y134.571 E19.34125
G1 X146.222 Y139.348 E19.97803
G1 X143.858 Y139.698 E20.07648
G1 X141.778 Y139.348 E20.16334
G1 X127.078 Y134.571 E20.80011
G1 X124.959 Y133.465 E20.89856
G1 X123.483 Y131.959 E20.98542
G1 X114.398 Y119.454 E21.62219
G1 X113.334 Y117.314 E21.72065
G1 X113.025 Y115.229 E21.8075
G1 X113.025 Y99.771 E22.44428
G1 X113.422 Y97.415 E22.54273
G1 X114.398 Y95.546 E22.62959
G1 X120.238 Y87.507 E23.03894
G1 X120.559 Y87.74 F7800
G1 F1800
G1 X123.804 Y83.274 E23.26636
G1 X125.47 Y81.656 E23.36204
G1 X127.2 Y80.806 E23.44144
G1 X141.901 Y76.029 E24.07822
G1 X144.2 Y75.7 E24.17389
G1 X146.099 Y76.029 E24.2533
G1 X160.8 Y80.806 E24.89007
G1 X162.853 Y81.891 E24.98575
G1 X164.196 Y83.274 E25.06515
G1 X173.282 Y95.779 E25.70193
G1 X174.306 Y97.863 E25.79761
G1 X174.579 Y99.771 E25.87701
G1 X174.579 Y115.229 E26.51378
G1 X174.182 Y117.517 E26.60946
G1 X173.282 Y119.221 E26.68887
G1 X164.196 Y131.726 E27.32564
G1 X162.53 Y133.344 E27.42132
G1 X160.8 Y134.194 E27.50072
G1 X146.099 Y138.971 E28.1375
G1 X143.8 Y139.3 E28.23317
G1 X141.901 Y138.971 E28.31258
G1 X127.2 Y134.194 E28.94935
G1 X125.147 Y133.109 E29.04503
G1 X123.804 Y131.726 E29.12443
G1 X114.718 Y119.221 E29.76121
G1 X113.694 Y117.137 E29.85689
G1 X113.421 Y115.229 E29.93629
G1 X113.421 Y99.771 E30.57306
G1 X113.818 Y97.483 E30.66874
G1 X114.718 Y95.779 E30.74814
G1 X120.524 Y87.788 E31.15503
G1 X120.844 Y88.021 F7800
G1 F1800
G1 X124.124 Y83.506 E31.38492
G1 X125.749 Y81.945 E31.47774
G1 X127.323 Y81.183 E31.54977
G1 X142.023 Y76.406 E32.18654
G1 X144.256 Y76.098 E32.27937
G1 X145.977 Y76.406 E32.35139
G1 X160.677 Y81.183 E32.98817
G1 X162.664 Y82.246 E33.08099
G1 X163.876 Y83.506 E33.15302
G1 X172.961 Y96.012 E33.78979
G1 X173.944 Y98.039 E33.88262
G1 X174.183 Y99.771 E33.95464
G1 X174.183 Y115.229 E34.59142
G1 X173.786 Y117.447 E34.68424
G1 X172.961 Y118.988 E34.75627
G1 X163.876 Y131.494 E35.39304
G1 X162.251 Y133.055 E35.48587
G1 X160.677 Y133.817 E35.55789
G1 X145.977 Y138.594 E36.19467
G1 X143.744 Y138.902 E36.28749
G1 X142.023 Y138.594 E36.35952
G1 X127.323 Y133.817 E36.99629
G1 X125.336 Y132.754 E37.08912
G1 X124.124 Y131.494 E37.16114
G1 X115.039 Y118.988 E37.79792
G1 X114.056 Y116.961 E37.89074
G1 X113.817 Y115.229 E37.96277
G1 X113.817 Y99.771 E38.59954
G1 X114.214 Y97.553 E38.69237
G1 X115.039 Y96.012 E38.76439
G1 X120.809 Y88.07 E39.16881
G1 E32.66881 F2400
G92 E0
G1 X130.588 Y97.945 F7800
G1 E6.5 F2400
;TYPE:Perimeter
;WIDTH:0.449999
G1 F1800
G1 X130.654 Y97.89 E6.50354
G1 X130.835 Y97.567 E6.51878
G1 X130.885 Y97.196 E6.53421
G1 X130.405 Y88.789 E6.88113
G1 X138.253 Y91.843 E7.22804
G1 X138.504 Y91.904 E7.23868
G1 X138.851 Y91.881 E7.25302
G1 X139.187 Y91.726 E7.26826
G1 X139.446 Y91.455 E7.2837
G1 X144 Y84.371 E7.63061
G1 X148.554 Y91.455 E7.97753
G1 X148.721 Y91.652 E7.98817
G1 X149.015 Y91.838 E8.00251
G1 X149.378 Y91.91 E8.01775
G1 X149.747 Y91.843 E8.03318
G1 X157.595 Y88.789 E8.3801
G1 X157.115 Y97.196 E8.72701
G1 X157.134 Y97.454 E8.73765
G1 X157.264 Y97.777 E8.75199
G1 X157.515 Y98.049 E8.76723
G1 X157.852 Y98.211 E8.78267
G1 X165.997 Y100.353 E9.12958
G1 X160.667 Y106.873 E9.47649
G1 X160.531 Y107.092 E9.48713
G1 X160.446 Y107.43 E9.50148
G1 X160.489 Y107.797 E9.51671
G1 X160.667 Y108.127 E9.53215
G1 X165.997 Y114.647 E9.87906
G1 X157.852 Y116.789 E10.22598
G1 X157.613 Y116.887 E10.23661
G1 X157.346 Y117.11 E10.25096
G1 X157.165 Y117.433 E10.2662
G1 X157.115 Y117.804 E10.28163
G1 X157.595 Y126.211 E10.62854
G1 X149.747 Y123.157 E10.97546
G1 X149.496 Y123.096 E10.9861
G1 X149.149 Y123.119 E11.00044
G1 X148.813 Y123.274 E11.01568
G1 X148.554 Y123.545 E11.03111
G1 X144 Y130.629 E11.37803
G1 X139.446 Y123.545 E11.72494
G1 X139.279 Y123.348 E11.73558
G1 X138.985 Y123.162 E11.74992
G1 X138.622 Y123.09 E11.76516
G1 X138.253 Y123.157 E11.7806
G1 X130.405 Y126.211 E12.12751
G1 X130.885 Y117.804 E12.47442
G1 X130.866 Y117.546 E12.48506
G1 X130.736 Y117.223 E12.49941
G1 X130.485 Y116.951 E12.51464
G1 X130.148 Y116.789 E12.53008
G1 X122.003 Y114.647 E12.87699
G1 X127.333 Y108.127 E13.2239
G1 X127.469 Y107.908 E13.23454
G1 X127.554 Y107.57 E13.24889
G1 X127.511 Y107.203 E13.26413
G1 X127.333 Y106.873 E13.27956
G1 X122.003 Y100.353 E13.62647
G1 X130.148 Y98.211 E13.97339
G1 X130.387 Y98.113 E13.98403
G1 X130.542 Y97.984 E13.99236
G1 X130.322 Y97.643 F7800
G1 F1800
G1 X130.431 Y97.511 E13.99943
G1 X130.489 Y97.219 E14.0117
G1 X129.975 Y88.196 E14.38401
G1 X138.397 Y91.473 E14.75632
G1 X138.618 Y91.514 E14.76558
G1 X138.894 Y91.443 E14.77731
G1 X139.113 Y91.241 E14.78958
G1 X144 Y83.638 E15.1619
G1 X148.887 Y91.241 E15.53421
G1 X149.042 Y91.403 E15.54347
G1 X149.307 Y91.508 E15.55521
G1 X149.603 Y91.473 E15.56747
G1 X158.025 Y88.196 E15.93978
G1 X157.511 Y97.219 E16.31209
G1 X157.541 Y97.441 E16.32135
G1 X157.693 Y97.682 E16.33309
G1 X157.953 Y97.827 E16.34536
G1 X166.694 Y100.126 E16.71767
G1 X160.974 Y107.124 E17.08998
G1 X160.867 Y107.322 E17.09924
G1 X160.849 Y107.606 E17.11098
G1 X160.974 Y107.876 E17.12324
G1 X166.694 Y114.874 E17.49555
G1 X157.953 Y117.173 E17.86786
G1 X157.751 Y117.27 E17.87712
G1 X157.569 Y117.489 E17.88886
G1 X157.511 Y117.781 E17.90113
G1 X158.025 Y126.804 E18.27344
G1 X149.603 Y123.527 E18.64575
G1 X149.382 Y123.486 E18.65501
G1 X149.106 Y123.557 E18.66674
G1 X148.887 Y123.759 E18.67901
G1 X144 Y131.361 E19.05132
G1 X139.113 Y123.759 E19.42363
G1 X138.958 Y123.597 E19.43289
G1 X138.693 Y123.492 E19.44463
G1 X138.397 Y123.527 E19.45689
G1 X129.975 Y126.804 E19.82921
G1 X130.489 Y117.781 E20.20152
G1 X130.459 Y117.559 E20.21078
G1 X130.307 Y117.318 E20.22251
G1 X130.047 Y117.173 E20.23478
G1 X121.306 Y114.874 E20.60709
G1 X127.026 Y107.876 E20.9794
G1 X127.133 Y107.678 E20.98866
G1 X127.151 Y107.394 E21.0004
G1 X127.026 Y107.124 E21.01266
G1 X121.306 Y100.126 E21.38497
G1 X130.047 Y97.827 E21.75728
G1 X130.249 Y97.73 E21.76655
G1 X130.283 Y97.689 E21.76874
G1 X130.033 Y97.396 F7800
;TYPE:External perimeter
G1 F1800
G1 X130.093 Y97.241 E21.77558
G1 X129.544 Y87.603 E22.17329
G1 X138.541 Y91.104 E22.571
G1 X138.639 Y91.116 E22.57508
G1 X138.779 Y91.026 E22.58192
G1 X144 Y82.906 E22.97964
G1 X149.221 Y91.026 E23.37735
G1 X149.294 Y91.094 E23.38144
G1 X149.459 Y91.104 E23.38827
G1 X158.456 Y87.603 E23.78598
G1 X157.907 Y97.241 E24.18369
G1 X157.926 Y97.339 E24.18778
G1 X158.054 Y97.444 E24.19462
G1 X167.391 Y99.9 E24.59233
G1 X161.281 Y107.375 E24.99003
G1 X161.239 Y107.465 E24.99412
G1 X161.281 Y107.625 E25.00096
G1 X167.391 Y115.1 E25.39867
G1 X158.054 Y117.556 E25.79638
G1 X157.967 Y117.604 E25.80046
G1 X157.907 Y117.759 E25.8073
G1 X158.456 Y127.397 E26.20501
G1 X149.459 Y123.896 E26.60272
G1 X149.361 Y123.884 E26.60681
G1 X149.221 Y123.974 E26.61365
G1 X144 Y132.094 E27.01135
G1 X138.779 Y123.974 E27.40906
G1 X138.706 Y123.906 E27.41315
G1 X138.541 Y123.896 E27.41999
G1 X129.544 Y127.397 E27.8177
G1 X130.093 Y117.759 E28.21541
G1 X130.074 Y117.661 E28.21949
G1 X129.946 Y117.556 E28.22633
G1 X120.609 Y115.1 E28.62404
G1 X126.719 Y107.625 E29.02175
G1 X126.761 Y107.535 E29.02584
G1 X126.719 Y107.375 E29.03268
G1 X120.609 Y99.9 E29.43038
G1 X129.98 Y97.425 E29.82966
G1 X130.196 Y97.368 F7800
;LAYER_CHANGE
;Z:0.45
;HEIGHT:0.2
G1 Z.45 F7800
M104 S212 ; set temperature
G1 X130.658 Y97.984
;TYPE:Perimeter
;WIDTH:0.449999
G1 F3600
G1 X130.714 Y97.937 E29.83215
G1 X130.901 Y97.603 E29.84507
G1 X130.951 Y97.218 E29.85822
G1 X130.427 Y88.819 E30.14309
G1 X138.254 Y91.913 E30.42795
G1 X138.514 Y91.977 E30.43702
G1 X138.873 Y91.954 E30.44921
G1 X139.22 Y91.794 E30.46214
G1 X139.487 Y91.512 E30.47529
G1 X144 Y84.408 E30.76016
G1 X148.513 Y91.512 E31.04503
G1 X148.685 Y91.717 E31.0541
G1 X148.99 Y91.909 E31.06629
G1 X149.364 Y91.984 E31.07921
G1 X149.746 Y91.913 E31.09236
G1 X157.573 Y88.819 E31.37723
G1 X157.049 Y97.218 E31.6621
G1 X157.067 Y97.485 E31.67116
G1 X157.201 Y97.82 E31.68335
G1 X157.46 Y98.1 E31.69628
G1 X157.811 Y98.267 E31.70943
G1 X165.961 Y100.364 E31.9943
G1 X160.6 Y106.852 E32.27916
G1 X160.458 Y107.079 E32.28823
G1 X160.37 Y107.428 E32.30042
G1 X160.414 Y107.807 E32.31334
G1 X160.6 Y108.148 E32.32649
G1 X165.961 Y114.636 E32.61136
G1 X157.811 Y116.733 E32.89623
G1 X157.563 Y116.833 E32.90529
G1 X157.286 Y117.063 E32.91748
G1 X157.099 Y117.397 E32.93041
G1 X157.049 Y117.782 E32.94356
G1 X157.573 Y126.181 E33.22843
G1 X149.746 Y123.087 E33.51329
G1 X149.486 Y123.023 E33.52236
G1 X149.127 Y123.046 E33.53455
G1 X148.78 Y123.206 E33.54747
G1 X148.513 Y123.488 E33.56062
G1 X144 Y130.591 E33.84549
G1 X139.487 Y123.488 E34.13036
G1 X139.315 Y123.283 E34.13942
G1 X139.01 Y123.091 E34.15161
G1 X138.636 Y123.016 E34.16454
G1 X138.254 Y123.087 E34.17769
G1 X130.427 Y126.181 E34.46255
G1 X130.951 Y117.782 E34.74742
G1 X130.933 Y117.515 E34.75649
G1 X130.799 Y117.18 E34.76868
G1 X130.54 Y116.9 E34.7816
G1 X130.189 Y116.733 E34.79475
G1 X122.039 Y114.636 E35.07962
G1 X127.4 Y108.148 E35.36449
G1 X127.542 Y107.921 E35.37355
G1 X127.63 Y107.572 E35.38574
G1 X127.586 Y107.193 E35.39867
G1 X127.4 Y106.852 E35.41182
G1 X122.039 Y100.364 E35.69668
G1 X130.189 Y98.267 E35.98155
G1 X130.437 Y98.167 E35.99062
G1 X130.612 Y98.022 E35.99829
G1 X130.385 Y97.671 F7800
G1 F3600
G1 X130.495 Y97.526 E36.00446
G1 X130.545 Y97.244 E36.01416
G1 X129.981 Y88.205 E36.32072
G1 X138.403 Y91.534 E36.62727
G1 X138.662 Y91.576 E36.63613
G1 X138.937 Y91.493 E36.64586
G1 X139.143 Y91.294 E36.65557
G1 X144 Y83.649 E36.96213
G1 X148.857 Y91.294 E37.26869