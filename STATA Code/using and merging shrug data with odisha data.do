cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Shrug Data\Test"

//convert village shp and dbf files to stata files. 
*spshape2dta village, replace saving(shrug_village)
//above code has been run once. We do not need to keep running it again every time we run this do file. 

//browse shp file 
use shrug_village_shp, clear

//browse dta file 
use shrug_village, clear

//create new village_id variable that will be used to merge with odisha dataset. 
gen village_id = pc11_tv_id
sort village_id 
quietly by village_id : gen dup = cond(_N == 1, 0, _n)
keep if dup <= 1
save "shrug_village.dta", replace

*import lgd
import excel "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\LGD\odisha_village_gp_mapping.xlsx", sheet("Sheet1") firstrow clear
rename VillageCode village_id
rename LocalBodyCode Local_Body_Code

*import shrug village dta file
cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Shrug Data"
merge 1:1 village_id using shrug_village
keep if _m == 3
drop _m

*save odisha shrug data merged with lgd data
cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Shrug Data"
save "odisha_shrug_village_lgd_merged.dta", replace

*import census lgd merged for odisha
import delimited "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Data Extraction From JJM\Odisha\LGD, Census merge\odisha_census_lgd_merged.csv", clear
rename localbodycode Local_Body_Code
drop _merge

sort village_id Local_Body_Code
quietly by village_id Local_Body_Code: gen dup = cond(_N == 1, 0, _n) 

keep if dup <= 1

cd "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Shrug Data"

*merge the odisha data file that was merged with census and LGD with another data file that merged the shrug data and the lgd data. Combine on LGD columns. 
merge 1:1 village_id Local_Body_Code using odisha_shrug_village_lgd_merged

save "C:\Users\savas\Documents\Ashoka\Courses\Development Economics\Dev Course Research\Merged Data\odisha_jjm_fully_merged.dta", replace


