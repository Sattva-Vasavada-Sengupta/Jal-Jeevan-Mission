import delimited "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Data Extraction From JJM\Odisha\LGD, Census merge\odisha_census_lgd_merged.csv", clear

tab p_sarpanch, gen(sarpanch_gen_)
tab ws_chairperson, gen(ws_cp_gen_)
tab ws_memsec, gen(ws_memsec_gen_)
tab ws_advisory_mem, gen(ws_advmem_gen_)
tab v232_11, gen(tank_pond_lake_)
tab v308_11, gen(allweather_road_)
tab v298_11, gen(maj_dist_road_)
tab v358_11, gen(powrsupp_domstuse_)
tab v214_11, gen(covered_well_)
tab v42_11, gen(govt_prim_sch_)
tab v49_11, gen(govt_midd_sch_)
tab v56_11, gen(govt_secnd_sch_)
tab v239_11, gen(open_drain_)
tab v253_11, gen(post_office_)

*rename variables to understand names easily
rename sarpanch_gen_1 sarpanch_woman
rename ws_cp_gen_1 ws_chairperson_woman
rename ws_memsec_gen_1 ws_memsec_woman
rename ws_advmem_gen_1 ws_advmem_woman
rename tank_pond_lake_1 tank_pond_lake
rename allweather_road_1 allweather_road
rename maj_dist_road_1 maj_dist_road
rename powrsupp_domstuse_1 powrsupp_domstuse
rename v359_11 powrsupp_summer_hrs 
rename v389_11 area_und_irrg 	
rename covered_well_1 covered_well
rename v24_11 tot_geo_area
rename govt_prim_sch_1 govt_prim_sch
rename govt_midd_sch_1 govt_midd_sch
rename govt_secnd_sch_1 govt_secnd_sch
rename open_drain_1 open_drainage
rename post_office_1 post_office
rename v25_11 total_hh_11
rename v19_11 distance_stat_town
rename v15_11 distance_subdist_hq
rename v17_11 distance_dist_hq

* allweather_road maj_dist_road powrsupp_domstuse powrsupp_summer_hrs area_und_irrg covered_well tot_geo_area govt_prim_sch govt_midd_sch govt_secnd_sch open_drainage post_office
*generate vars and dummies
*v223_11 - 1, if yes borewell, 2 if not, . if nan. 
gen tube_borewell = 0
replace tube_borewell = 1 if v223_11 == 1
replace tube_borewell = . if v223_11 == .

gen ln_total_hh_11 = log(total_hh_11)
gen ln_distance_stat_town = log(distance_stat_town)
gen ln_distance_dist_hq = log(distance_dist_hq)
gen ln_tot_geo_area = log(tot_geo_area)

replace area_und_irrg = 1 if area_und_irrg == 0
gen ln_area_und_irrg = log(area_und_irrg)

gen sex_ratio = tot_f_11/ tot_m_11

*define controls 
global controls ln_total_hh_11 tank_pond_lake tube_borewell ln_distance_stat_town ln_distance_dist_hq allweather_road maj_dist_road powrsupp_domstuse ln_area_und_irrg covered_well ln_tot_geo_area open_drainage post_office sex_ratio 

global controls_fortables total_hh_11 tank_pond_lake tube_borewell distance_stat_town distance_dist_hq allweather_road maj_dist_road powrsupp_domstuse area_und_irrg covered_well tot_geo_area open_drainage post_office sex_ratio 

*summary statistics
cd "G:/My Drive/JJM Dev Econ/Tables"

*keeping and dropping
sort village_id
quietly by village_id: gen dup = cond(_N == 1, 0, _n)

gen dup_balance = 1 if dup > 1 
replace dup_balance = 0 if dup <= 1

balancetable dup_balance $controls_fortables  using "village_id_dup_balance.tex",  ctitles("Duplicate = 0" "Duplicate = 1" "Difference") oneline nonumbers replace

keep if dup <= 1 //does not change coefficents that much, nor does it make significant things insignificant or vica-versa. 

drop dup dup_balance
sort village_name districtname
quietly by village_name districtname: gen dup = cond(_N == 1, 0, _n)

gen dup_balance = 1 if dup > 0
replace dup_balance = 0 if dup == 0

balancetable dup_balance $controls_fortables  using "village_name_dup_balance.tex", ctitles("Duplicate = 0" "Duplicate = 1" "Difference") oneline nonumbers replace

keep if dup == 0

*summary statistics
cd "G:/My Drive/JJM Dev Econ/Tables"
*data summary_stats
estpost sum sarpanch_woman ws_chairperson_woman ws_memsec_woman $controls_fortables
esttab . using "summary_stats.rtf", cells ("count mean sd min max") noobs replace

*get correlation tables between three main explanatory variables.
corr sarpanch_woman ws_chairperson_woman ws_memsec_woman

*for balance tables, we use ssc install balancetable
*balance over Female Sarpanch
balancetable sarpanch_woman ws_chairperson_woman ws_memsec_woman $controls_fortables  using "fem_sarpanch_covariate_balance.tex", ctitles("Female = 0" "Female = 1" "Difference") oneline nonumbers prehead("\tiny" "\begin{tabular}{l*{3}c}" "\hline\hline") replace

balancetable ws_chairperson_woman sarpanch_woman ws_memsec_woman $controls_fortables  using "fem_ws_cp_covariate_balance.tex", ctitles("Female = 0" "Female = 1" "Difference") oneline nonumbers prehead("\tiny" "\begin{tabular}{l*{3}c}" "\hline\hline") replace

balancetable ws_memsec_woman ws_chairperson_woman sarpanch_woman $controls_fortables  using "fem_ws_memsec_covariate_balance.tex", ctitles("Female = 0" "Female = 1" "Difference") oneline nonumbers prehead("\tiny" "\begin{tabular}{l*{3}c}" "\hline\hline") replace

*regressions
reg tap_perc_hh sarpanch_woman, robust
eststo r1 
estadd local fixed "no" , replace
estadd local controls "no", replace

reg tap_perc_hh sarpanch_woman ws_chairperson_woman, robust
eststo r2 
estadd local fixed "no" , replace
estadd local controls "no", replace

reg tap_perc_hh sarpanch_woman##ws_chairperson_woman, robust
eststo r3 
estadd local fixed "no" , replace
estadd local controls "no", replace

reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman, absorb(districtcode) vce(robust)
eststo r4 
estadd local fixed "district" , replace
estadd local controls "no", replace

reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman, absorb(subdistrictcode) vce(robust)
eststo r5 
estadd local fixed "subdistrict" , replace
estadd local controls "no", replace

reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman, absorb(localbodycode) vce(robust)
eststo r6
estadd local fixed "local body(GP)" , replace
estadd local controls "no", replace

reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(subdistrictcode) vce(robust)
eststo r7
estadd local fixed "subdistrict" , replace
estadd local controls "yes", replace

reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(localbodycode) vce(robust) 
eststo r8
estadd local fixed "local body(GP)" , replace
estadd local controls "yes", replace


*robustness check: model variation teset: http://www.polsci.org/robustness/robustness.pdf

*robustness by: 1) coastal districts
preserve 
drop if districtname == "baleshwar" | districtname == "bhadrak" | districtname == "jajapur" |districtname == "kendrapara" |districtname == "rayagada" |districtname == "cuttack" |districtname =="jagatsinghapur" |districtname =="puri" 
reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(subdistrictcode) vce(robust)
eststo rc1
estadd local rbc "Coastal (5)"
restore

*2) high elevation districts
preserve 
drop if districtname == "malkangiri" | districtname == "koraput" | districtname == "rayagadapur" |districtname == "nabarangpur" |districtname == "gajapati" |districtname == "nuapada" 
reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(subdistrictcode) vce(robust)
eststo rc2
estadd local rbc "H Elev (5)"
restore

*3) high total domestic product districts
preserve 
drop if districtname == "sundargarh" | districtname == "khordha" | districtname == "ganjam" |districtname == "cuttack" |districtname == "angul" 
reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(subdistrictcode) vce(robust)
eststo rc3
estadd local rbc "H GDP (5)"
restore

*4) lowest total domestic product districts
preserve 
drop if districtname == "nuapada" | districtname == "sonepur" | districtname == "malkangiri" |districtname == "boudh" |districtname == "deogarh" 
reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(subdistrictcode) vce(robust)
eststo rc4
estadd local rbc "L GDP (5)"
restore

*5) lowest and highest total domestic product districts
preserve 
drop if districtname == "sundargarh" | districtname == "khordha" | districtname == "ganjam" |districtname == "cuttack" |districtname == "angul" | districtname == "nuapada" | districtname == "sonepur" | districtname == "malkangiri" |districtname == "boudh" |districtname == "deogarh" 
reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls, absorb(subdistrictcode) vce(robust)
eststo rc5
estadd local rbc "L\&H GDP (10)"
restore

*5) each district 
levelsof districtname, local(levels) 
foreach district of local levels {
	di "`district'"
	quietly reghdfe tap_perc_hh sarpanch_woman##ws_chairperson_woman $controls if districtname == "`district'", absorb(subdistrictcode)  
	esttab, keep (1.sarpanch_woman 1.ws_chairperson_woman 1.sarpanch_woman#1.ws_chairperson_woman) p
}

*Esttabing stuff
cd "G:/My Drive/JJM Dev Econ/Tables"

*No interaction terms, no controls, no fixed effects
esttab r1 r2 using "jjm_noInteract.tex", keep(sarpanch_woman ws_chairperson_woman) se(3) s(fixed controls N, label("fixed effects" "controls")) varlabels (sarpanch_woman "Woman Sarpanch" ws_chairperson_woman "Woman WS CP ")  star(* 0.10 ** 0.05 *** 0.01) replace	

*interactions + controls + fixed effects - does not include GP equation - 
esttab r3 r4 r5 r7 using "jjm_regtable_main_noGP.tex", keep(1.sarpanch_woman 1.ws_chairperson_woman 1.sarpanch_woman#1.ws_chairperson_woman) se(3) s(fixed controls N, label("fixed effects" "controls")) varlabels (1.sarpanch_woman "Woman Sarpanch" 1.ws_chairperson_woman "Woman WS CP " 1.sarpanch_woman#1.ws_chairperson_woman "Woman (Sarpanch * WS CP)") star(* 0.10 ** 0.05 *** 0.01) replace

cd "G:/My Drive/JJM Dev Econ/Tables"

*Robustness checks
esttab rc1 rc2 rc3 rc4 rc5 using "jjm_robustness_checks.tex", keep(1.sarpanch_woman 1.ws_chairperson_woman 1.sarpanch_woman#1.ws_chairperson_woman) se(3) s(rbc N, label("Dropped Districts: ")) varlabels (1.sarpanch_woman "Woman Sarpanch" 1.ws_chairperson_woman "Woman WS CP " 1.sarpanch_woman#1.ws_chairperson_woman "Woman (Sarpanch * WS CP)") star(* 0.10 ** 0.05 *** 0.01) replace

