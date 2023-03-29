*A: Merging original JJM with LGD data. There seem to be two versions of A. One is a normal merge, and the other is a merge with cleaned village codes and names. 
*B: Merging A with Census data. 
*C Merging B with Shrug data

*A: analyse original JJM and LGD merging: naive merging. We do not use this file to merge with census. This section is which 79 districts were not merged and their characterisitcs. 
import delimited "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Data Extraction From JJM\Odisha\LGD, Census merge\odisha_lgd_merged.csv", clear

tab p_sarpanch, gen(sarpanch_gen_)
tab ws_chairperson, gen(ws_cp_gen_)
tab ws_memsec, gen(ws_memsec_gen_)

rename sarpanch_gen_1 sarpanch_woman
rename ws_cp_gen_1 ws_chairperson_woman
rename ws_memsec_gen_1 ws_memsec_woman

gen match = 1
replace match = 0 if districtcensus2011code == .


balancetable match sarpanch_woman ws_chairperson_woman ws_memsec_woman tap_perc_hh using "od_jjm_lgd_notmerged_analysis.tex", ctitles("Merged = 0" "Merged = 1" "Difference") oneline nonumbers prehead("\tiny" "\begin{tabular}{l*{3}c}" "\hline\hline") replace

sort village_id
quietly by village_id: gen dup = cond(_N == 1, 0, _n)

tab dup

gen dup_dummy = 0
replace dup_dummy = 1 if dup > 0

preserve 
keep if dup <= 1
cd "G:/My Drive/JJM Dev Econ/Tables"
balancetable dup_dummy sarpanch_woman ws_chairperson_woman ws_memsec_woman tap_perc_hh using "od_jjm_lgd_duplicate_analysis.xlsx", replace
restore

*observe that there are 43556 unique matches, and around 2800 matches which are duplicates. I then go to python and try finding actual village codes using village names within a district. 

**********************************************************************************************************************************************************************************************

*A: analyse original JJM and LGD merging: naive merging + fuzzy matching the duplicate values on top. This is what we are using for merging with census. 
import delimited "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Data Extraction From JJM\Odisha\LGD, Census merge\odisha_lgd_merged_cleaned.csv", clear

tab p_sarpanch, gen(sarpanch_gen_)
tab ws_chairperson, gen(ws_cp_gen_)
tab ws_memsec, gen(ws_memsec_gen_)

rename sarpanch_gen_1 sarpanch_woman
rename ws_cp_gen_1 ws_chairperson_woman
rename ws_memsec_gen_1 ws_memsec_woman


sort village_id
quietly by village_id: gen dup = cond(_N == 1, 0, _n)

tab dup

gen dup_dummy = 0
replace dup_dummy = 1 if dup > 0

preserve 
keep if dup <= 1
cd "G:/My Drive/JJM Dev Econ/Tables"
balancetable dup_dummy sarpanch_woman ws_chairperson_woman ws_memsec_woman tap_perc_hh using "od_jjm_lgd_cleaned_duplicate_analysis.xlsx", replace
restore

**********************************************************************************************************************************************************************************************


*B: Analysing A(2) merging with census data. 
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

*define controls 
global controls ln_total_hh_11 tank_pond_lake tube_borewell ln_distance_stat_town ln_distance_dist_hq allweather_road maj_dist_road powrsupp_domstuse ln_area_und_irrg covered_well ln_tot_geo_area open_drainage post_office

global controls_fortables total_hh_11 tank_pond_lake tube_borewell distance_stat_town distance_dist_hq allweather_road maj_dist_road powrsupp_domstuse area_und_irrg covered_well tot_geo_area open_drainage post_office


gen match = 1
replace match = 0 if tot_p_11 == .
*choose a variable that is available for all villages in census. Total population in 2011 is a good one. 
balancetable match sarpanch_woman ws_chairperson_woman ws_memsec_woman tap_perc_hh using "od_jjm_lgd_census_notmerged_analysis.tex", ctitles("Merged = 0" "Merged = 1" "Difference") oneline nonumbers replace


sort village_id
quietly by village_id: gen dup = cond(_N == 1, 0, _n)

tab dup

gen dup_dummy = 0
replace dup_dummy = 1 if dup > 0

preserve 
keep if dup <= 1
cd "G:/My Drive/JJM Dev Econ/Tables"
balancetable dup_dummy sarpanch_woman ws_chairperson_woman ws_memsec_woman tap_perc_hh $controls_fortables using "od_jjm_lgd_cleaned_census_duplicate_analysis.xlsx", replace
restore
