"""Build schools.csv: one row per PPS school/program relevant to assignment + scenarios.
Sources: ODE Fall Membership 2025-26 (grades), PSU PRC forecast Table 5.5 (program split, 2025-26),
meub/pps-data pps_schools.csv (NCES id, lat/lon, capacity, DLI language), PPS immersion report Oct 2025,
PPS Family Guides Oct 2026 (2031-32 projections, renames)."""
import pathlib, json, numpy as np, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
R = D / "raw/meub-pps-data/data"
ode = pd.read_excel(R / "raw/fall_membership_2025_26.xlsx", "School 20252026")
ode = ode[ode["District Name"] == "Portland SD 1J"]
gcols = [c for c in ode.columns if "Kindergarten" in c or "Grade" in c]
ode = ode[["School Institution ID", "School Name", "School Type", "2025-26 Total Enrollment"] + gcols]
ode.columns = ["ode_id", "ode_name", "ode_type", "enr_total"] + ["g_K"] + [f"g_{i}" for i in range(1, 13)]
mb = pd.read_csv(R / "pps_schools.csv")
fc = pd.read_csv(R / "raw/pps_enrollment_forecast.csv")
# canonical, level, grades, ode_name, meub_name, fc_name, es_area(model name), ms_area, hs_area, focus, notes
S = [
 # K-5 / K-8 neighborhood
 ("Abernethy","K-5","K-5","Abernethy Elementary School","Abernethy Elementary School","Abernethy","Abernethy",None,None,0,""),
 ("Ainsworth","K-5","K-5","Ainsworth Elementary School","Ainsworth Elementary School","Ainsworth","Ainsworth",None,None,0,""),
 ("Alameda","K-5","K-5","Alameda Elementary School","Alameda Elementary School","Alameda","Alameda",None,None,0,""),
 ("Arleta","K-5","K-5","Arleta Elementary School","Arleta Elementary School","Arleta","Arleta",None,None,0,""),
 ("Astor","K-8","K-8","Astor Elementary School","Astor Elementary School","Astor","Astor","Astor",None,0,""),
 ("Atkinson","K-5","K-5","Atkinson Elementary School","Atkinson Elementary School","Atkinson","Atkinson",None,None,0,""),
 ("Beach","K-5","K-5","Beach Elementary School","Beach Elementary School","Beach","Beach",None,None,0,""),
 ("Beverly Cleary","K-8","K-8","Beverly Cleary School ","Beverly Cleary School ","BeverlyCleary","Beverly Cleary","Beverly Cleary",None,0,"Two campuses (Fernwood/Hollyrood)"),
 ("Boise-Eliot/Humboldt","K-5","K-5","Boise-Eliot Elementary School","Boise-Eliot Elementary School","Boise-Eliot/Humboldt","Boise-Eliot/Humboldt",None,None,0,""),
 ("Bridger","K-8","K-8","Bridger Creative Science School","Bridger Creative Science School","BridgerCreativeScience","Bridger","Bridger",None,0,"Neighborhood area + Creative Science focus lottery (share not published)"),
 ("Bridlemile","K-5","K-5","Bridlemile Elementary School","Bridlemile Elementary School","Bridlemile","Bridlemile",None,None,0,""),
 ("Buckman","K-5","K-5","Buckman Elementary School","Buckman Elementary School","Buckman","Buckman",None,None,0,"Neighborhood + arts focus option (lottery share not published)"),
 ("Capitol Hill","K-5","K-5","Capitol Hill Elementary School","Capitol Hill Elementary School","Capitol Hill","Capitol Hill",None,None,0,""),
 ("Cesar Chavez","K-8","K-8","César Chávez K-8 School","César Chávez K-8 School","César Chávez","Cesar Chavez","Cesar Chavez",None,0,""),
 ("Chapman","K-5","K-5","Chapman Elementary School","Chapman Elementary School","Chapman","Chapman",None,None,0,""),
 ("Chief Joseph","K-5","K-5","Chief Joseph Elementary School","Chief Joseph Elementary School","ChiefJoseph","Chief Joseph",None,None,0,""),
 ("Clark","K-5","K-5","Clark Elementary School","Clark Elementary School","Clark","Clark",None,None,0,"Opened 2023 at Binnsmead; no NCES id in CCD 2022"),
 ("Creston","K-5","K-5","Creston Elementary School","Creston Elementary School","Creston","Creston",None,None,0,"Hosts regional Deaf/Hard of Hearing program"),
 ("Duniway","K-5","K-5","Duniway Elementary School","Duniway Elementary School","Duniway","Duniway",None,None,0,""),
 ("Faubion","K-8","K-8","Faubion Elementary School","Faubion Elementary School","Faubion","Faubion","Faubion",None,0,""),
 ("Forest Park","K-5","K-5","Forest Park Elementary School","Forest Park Elementary School","ForestPark","Forest Park",None,None,0,""),
 ("Glencoe","K-5","K-5","Glencoe Elementary School","Glencoe Elementary School","Glencoe","Glencoe",None,None,0,""),
 ("Grout","K-5","K-5","Grout Elementary School","Grout Elementary School","Grout","Grout",None,None,0,""),
 ("Hayhurst","K-5","K-5","Hayhurst Elementary School","Hayhurst Elementary School","Hayhurst","Hayhurst",None,None,0,"ODE row includes Odyssey K-8 program (same building); Hayhurst neighborhood = PRC Table 5.5"),
 ("Irvington","K-5","K-5","Irvington Elementary School","Irvington Elementary School","Irvington","Irvington",None,None,0,""),
 ("James John","K-5","K-5","James John Elementary School","James John Elementary School","JamesJohn","James John",None,None,0,""),
 ("Kelly","K-5","K-5","Kelly Elementary School","Kelly Elementary School","Kelly","Kelly",None,None,0,""),
 ("Laurelhurst","K-8","K-8","Laurelhurst Elementary School","Laurelhurst Elementary School","Laurelhurst","Laurelhurst","Laurelhurst",None,0,""),
 ("Lee (Sunrise)","K-5","K-5","Lee Elementary School","Lee Elementary School","Lee","Lee",None,None,0,"Renamed Sunrise in the Oct-2026 family guides (projections match PRC 'Lee')"),
 ("Lent","K-5","K-5","Lent Elementary School","Lent Elementary School","Lent","Lent",None,None,0,"Whole-school Spanish DLI that also has a neighborhood area"),
 ("Lewis","K-5","K-5","Lewis Elementary School","Lewis Elementary School","Lewis","Lewis",None,None,0,""),
 ("Llewellyn","K-5","K-5","Llewellyn Elementary School","Llewellyn Elementary School","Llewellyn","Llewellyn",None,None,0,""),
 ("MLK Jr","K-5","K-5","Dr. Martin Luther King Jr. School","Dr. Martin Luther King Jr. School","MLKJr","MLK Jr",None,None,0,""),
 ("Maplewood","K-5","K-5","Maplewood Elementary School","Maplewood Elementary School","Maplewood","Maplewood",None,None,0,""),
 ("Markham","K-5","K-5","Markham Elementary School","Markham Elementary School","Markham","Markham",None,None,0,""),
 ("Marysville","K-5","K-5","Marysville Elementary School","Marysville Elementary School","Marysville","Marysville",None,None,0,"K-5 in 2025-26 (meub lists k8)"),
 ("Peninsula","K-5","K-5","Peninsula Elementary School","Peninsula Elementary School","Peninsula","Peninsula",None,None,0,""),
 ("Rieke","K-5","K-5","Rieke Elementary School","Rieke Elementary School","Rieke","Rieke",None,None,0,""),
 ("Rigler","K-5","K-5","Rigler Elementary School","Rigler Elementary School","Rigler","Rigler",None,None,0,"Whole-school Spanish DLI that also has a neighborhood area"),
 ("Rosa Parks","K-5","K-5","Rosa Parks Elementary School","Rosa Parks Elementary School","RosaParks","Rosa Parks",None,None,0,""),
 ("Rose City Park","K-5","K-5","Rose City Park","Rose City Park","RoseCityPark","Rose City Park",None,None,0,""),
 ("Sabin","K-5","K-5","Sabin Elementary School","Sabin Elementary School","Sabin","Sabin",None,None,0,""),
 ("Scott","K-5","K-5","Scott Elementary School","Scott Elementary School","Scott","Scott",None,None,0,""),
 ("Sitton","K-5","K-5","Sitton Elementary School","Sitton Elementary School","Sitton","Sitton",None,None,0,""),
 ("Skyline","K-8","K-8","Skyline Elementary School","Skyline Elementary School","Skyline","Skyline","Skyline",None,0,""),
 ("Stephenson","K-5","K-5","Stephenson Elementary School","Stephenson Elementary School","Stephenson","Stephenson",None,None,0,""),
 ("Sunnyside","K-8","K-8","Sunnyside Environmental School","Sunnyside Environmental School","SunnysideEnvironmental","Sunnyside","Sunnyside",None,0,"Neighborhood area + environmental focus lottery (share not published; A/B discontinue the focus)"),
 ("Vernon","K-8","K-8","Vernon Elementary School","Vernon Elementary School","Vernon","Vernon","Vernon",None,0,""),
 ("Vestal","K-5","K-5","Vestal Elementary School","Vestal Elementary School","Vestal","Vestal",None,None,0,""),
 ("Whitman","K-5","K-5","Whitman Elementary School","Whitman Elementary School","Whitman","Whitman",None,None,0,""),
 ("Woodlawn","K-5","K-5","Woodlawn Elementary School","Woodlawn Elementary School","Woodlawn","Woodlawn",None,None,0,""),
 ("Woodmere","K-5","K-5","Woodmere Elementary School","Woodmere Elementary School","Woodmere","Woodmere",None,None,0,""),
 ("Woodstock","K-5","K-5","Woodstock Elementary School","Woodstock Elementary School","Woodstock","Woodstock",None,None,0,""),
 # middle
 ("Beaumont","6-8","6-8","Beaumont Middle School","Beaumont Middle School","Beaumont",None,"Beaumont",None,0,""),
 ("George","6-8","6-8","George Middle School","George Middle School","George",None,"George",None,0,""),
 ("Gray","6-8","6-8","Gray Middle School","Gray Middle School","Gray",None,"Gray",None,0,"'Robert Gray' in scenario docs"),
 ("Tubman","6-8","6-8","Harriet Tubman Middle School","Harriet Tubman Middle School","HarrietTubman",None,"Tubman",None,0,""),
 ("Harrison Park","6-8","6-8","Harrison Park School","Harrison Park School","HarrisonPark",None,"Harrison Park",None,0,""),
 ("Hosford","6-8","6-8","Hosford Middle School","Hosford Middle School","Hosford",None,"Hosford",None,0,""),
 ("Jackson","6-8","6-8","Jackson Middle School","Jackson Middle School","Jackson",None,"Jackson",None,0,""),
 ("Kellogg","6-8","6-8","Kellogg Middle School","Kellogg Middle School","Kellogg",None,"Kellogg",None,0,""),
 ("Lane (Brentwood)","6-8","6-8","Lane Middle School","Lane Middle School","Lane",None,"Lane",None,0,"Renamed Brentwood Middle School (2026)"),
 ("Mt Tabor","6-8","6-8","Mt Tabor Middle School","Mt Tabor Middle School","MtTabor",None,"Mt Tabor",None,0,""),
 ("Ockley Green","6-8","6-8","Ockley Green Middle School","Ockley Green Middle School","Ockley Green",None,"Ockley Green",None,0,""),
 ("Roseway Heights","6-8","6-8","Roseway Heights School","Roseway Heights School","RosewayHeights",None,"Roseway Heights",None,0,""),
 ("Sellwood","6-8","6-8","Sellwood Middle School","Sellwood Middle School","Sellwood",None,"Sellwood",None,0,""),
 ("West Sylvan","6-8","6-8","West Sylvan Middle School","West Sylvan Middle School","WestSylvan",None,"West Sylvan",None,0,""),
 # high
 ("Cleveland","9-12","9-12","Cleveland High School","Cleveland High School","Cleveland",None,None,"Cleveland",0,""),
 ("Franklin","9-12","9-12","Franklin High School","Franklin High School","Franklin",None,None,"Franklin",0,""),
 ("Grant","9-12","9-12","Grant High School","Grant High School","Grant",None,None,"Grant",0,""),
 ("Ida B. Wells","9-12","9-12","Ida B. Wells-Barnett High School","Ida B. Wells-Barnett High School","IdaBWells-Barnett",None,None,"Ida B. Wells",0,""),
 ("Jefferson","9-12","9-12","Jefferson High School","Jefferson High School","Jefferson",None,None,"Jefferson",0,"2025-26: dual-assignment zones (Jefferson/Grant, /McDaniel, /Roosevelt); own boundary phases in from 2026-27"),
 ("Lincoln","9-12","9-12","Lincoln High School","Lincoln High School","Lincoln",None,None,"Lincoln",0,""),
 ("McDaniel","9-12","9-12","Leodis V. McDaniel High School","Leodis V. McDaniel High School","McDaniel",None,None,"McDaniel",0,"Also PISA newcomer program"),
 ("Roosevelt","9-12","9-12","Roosevelt High School","Roosevelt High School","Roosevelt",None,None,"Roosevelt",0,"Also PISA newcomer program"),
 # focus / option / alternative (no attendance area)
 ("Winterhaven","focus K-8","K-8","Winterhaven School","Winterhaven School","Winterhaven",None,None,None,1,"STEM focus option, citywide lottery"),
 ("da Vinci","focus 6-8","6-8","da Vinci Middle School","da Vinci Middle School","daVinci",None,None,None,1,"Arts focus option, citywide lottery (PRC labels grades K-12 in error)"),
 ("Richmond","focus K-5 (DLI)","K-5","Richmond Elementary School","Richmond Elementary School","Richmond",None,None,None,1,"Whole-school Japanese DLI, no attendance area"),
 ("Odyssey","focus K-8","K-8",None,"Odyssey Program (K-8)","Odyssey",None,None,None,1,"Housed at East Sylvan/Hayhurst; ODE reports inside Hayhurst"),
 ("ACCESS","focus 1-8 (TAG)","1-8",None,"ACCESS Academy","ACCESS",None,None,None,1,"Not a separate ODE school; PRC count 324"),
 ("MLC","focus K-12 (alt)","K-12","Metropolitan Learning Center","Metropolitan Learning Center","MLC",None,None,None,1,"K-12 alternative; A/B make it K-8"),
 ("Benson","focus 9-12 (CTE)","9-12","Benson Polytechnic High School","Benson Polytechnic High School","BensonPolytechnic",None,None,None,1,"Citywide CTE high school"),
 ("Alliance","alternative 9-12","9-12","Alliance High School","Alliance High School",None,None,None,None,1,"Alternative HS"),
]
cols = ["name","level","grades","ode_name","meub_name","fc_name","es_area","ms_area","hs_area","focus_option","notes"]
s = pd.DataFrame(S, columns=cols)
s = s.merge(ode, on="ode_name", how="left")
m = mb.set_index("school_name")
for c_out, c_in in [("nces_id","nces_school_id"),("lat","latitude"),("lon","longitude"),("capacity_functional_2021","functional_capacity_2021"),
                    ("capacity_functional_model","functional_capacity_model"),("utilization_pct_2526_meub","utilization_pct_2526"),
                    ("dli_languages","dli_languages"),("dli_students_2526_report","dli_students_2526"),("seismic_status","seismic_retrofit_status"),
                    ("is_urm_building","is_urm_building"),("forecast_2031_32_prc","enrollment_forecast_2031_32")]:
    s[c_out] = s.meub_name.map(m[c_in])
s["nces_id"] = s.nces_id.map(lambda v: "" if pd.isna(v) else str(int(v)))
# Odyssey shares Hayhurst building coords? meub has its own row coords
# PRC Table 5.5 program rows (2025-26)
f = fc[["school_name","program","grades","hist_2025_26"]].copy()
f["school_name"] = f.school_name.str.replace(" ", "")
def prc(fcname, program):
    r = f[(f.school_name == fcname.replace(" ", "")) & (f.program == program)]
    return float(r.hist_2025_26.iloc[0]) if len(r) else np.nan
s["prc_total_2526"] = [prc(n, "Total") if isinstance(n, str) else np.nan for n in s.fc_name]
s["prc_neighborhood_2526"] = [prc(n, "Neighborhood") if isinstance(n, str) else np.nan for n in s.fc_name]
dli = f[~f.program.isin(["Total", "Neighborhood", "PISA"])]
s["prc_dli_2526"] = [dli[dli.school_name == n.replace(" ", "")].hist_2025_26.sum() if isinstance(n, str) else 0 for n in s.fc_name]
s["prc_dli_programs"] = [";".join(f"{r.program}:{int(r.hist_2025_26)}" for r in dli[dli.school_name == n.replace(" ", "")].itertuples()) if isinstance(n, str) else "" for n in s.fc_name]
s["prc_pisa_2526"] = [prc(n, "PISA") if isinstance(n, str) else np.nan for n in s.fc_name]
# fill missing enrollment for programs not separate in ODE
s.loc[s.name == "Odyssey", "enr_total"] = 217; s.loc[s.name == "ACCESS", "enr_total"] = 324
g = ["g_K"] + [f"g_{i}" for i in range(1, 13)]
s["enr_k5"] = s[g[:6]].sum(axis=1, min_count=1); s["enr_68"] = s[g[6:9]].sum(axis=1, min_count=1); s["enr_912"] = s[g[9:]].sum(axis=1, min_count=1)
# Hayhurst ODE row includes Odyssey (K-8, 217): split
hk5 = s.loc[s.name == "Hayhurst", "enr_k5"].iloc[0]
s.loc[s.name == "Odyssey", ["enr_k5", "enr_68"]] = [hk5 - 290, 77]
s.loc[s.name == "Hayhurst", ["enr_total", "enr_k5", "enr_68"]] = [290, 290, 0]
for gc in g: s.loc[s.name == "Hayhurst", gc] = np.nan  # grade detail mixed with Odyssey
s.to_csv(D / "work/schools_base.csv", index=False)
print(s[["name","level","ode_id","nces_id","enr_total","enr_k5","enr_68","enr_912","prc_total_2526","prc_neighborhood_2526","prc_dli_2526","capacity_functional_2021"]].to_string())
