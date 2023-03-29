cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Merged Data"


use odisha_jjm_fully_merged, clear
drop dup
keep if _merge == 3
sort village_id
quietly by village_id: gen dup = cond(_N == 1, 0, _n)

*preserve
keep if dup <= 1 //does not change coefficents that much, nor does it make significant things insignificant or vica-versa. 


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


*summary statistics
cd "G:/My Drive/JJM Dev Econ/Tables"
*data summary_stats
estpost sum sarpanch_woman ws_chairperson_woman ws_memsec_woman $controls_fortables
esttab . using "summary_stats.rtf", cells ("count mean sd min max") noobs replace

*get correlation tables between three main explanatory variables.
corr sarpanch_woman ws_chairperson_woman ws_memsec_woman

*for balance tables, we use ssc install balancetable
*balance over Female Sarpanch
balancetable sarpanch_woman ws_chairperson_woman ws_memsec_woman $controls_fortables  using "fem_sarpanch_covariate_balance.xlsx", replace


*regressions
reg tap_perc_hh sarpanch_woman
reg tap_perc_hh sarpanch_woman ws_chairperson_woman
reg tap_perc_hh sarpanch_woman ws_chairperson_woman ws_memsec_woman
reg tap_perc_hh sarpanch_woman##ws_chairperson_woman##ws_memsec_woman
reg tap_perc_hh sarpanch_woman##ws_chairperson_woman##ws_memsec_woman, absorb(districtcode) robust

reg tap_perc_hh sarpanch_woman##ws_chairperson_woman sarpanch_woman##ws_memsec_woman $controls, absorb(districtcode) robust


reg tap_perc_hh sarpanch_woman##ws_chairperson_woman##ws_memsec_woman $controls, absorb(districtcode) robust



cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Graphs"
local distlistloop angul balangir balasore

gen distnames = strproper(district)

levelsof distnames, local(levels)
*Graphs section. 
foreach dist of local levels{
	preserve 
	keep if distnames == "`dist'"
	cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Shrug Data"
	spmap tap_perc_hh using "shrug_village_shp", id(_ID) clmethod(custom) clbreaks(0 10 25 40 60 80 100) fcolor(RdBu) osize(thin) opattern(none) ndocolor(red) ndlabel("nan") ///
		legend(pos(6) row(3) ring(1) size(*0.75)) title("Odisha District: `dist'" "Percent of HH with tap-water", size(medsmall))
	cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Graphs"
	graph export "tap_per_hh_`dist'.png", replace
		
	restore
} 

levelsof distnames, local(levels)
foreach dist of local levels{
	preserve 
	keep if distnames == "`dist'" & distnames != "Jharsuguda"
	cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Shrug Data"
	spmap ws_chairperson_woman using "shrug_village_shp", id(_ID) fcolor(Set1) osize(thin) opattern(none) ndocolor(red) ndlabel("nan") ///
		legend(pos(6) row(3) ring(1) size(*0.75)) title("Odisha District: `dist'" "Water Samiti Chairperson" "Female (1), Male (0)", size(medsmall))
	cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Graphs"
	graph export "ws_cp_fem_`dist'.png", replace
		
	restore
}
