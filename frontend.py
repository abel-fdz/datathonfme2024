import streamlit as st
import csv
from streamlit_folium import st_folium
import folium
import t2_demo

class Characteristics:
    LotFeatures:list[str]
    LotSizeSquareFeet:int # SI

class ImageData:
    c1c6:float #SI FET
    q1q6:float #SI FET
    features_reso:list[str]
    room_type_reso:list[str]
    class style:
        exterior:str #SI FET
        stories:str #SI FET

class Listing:
    class Dates:
        CloseDate:str
    ListingId:str #SI FET
    class Price:
        ClosePrice:int #SI FET

    City:str #SI FET
    CountyOrParish:str #SI FET
    PostalCode:int #SI FET
    PostalCodePlus4:int
    StateOrProvince:str #SI FET
    StreetDirectionPrefix:str
    StreetDirectionSuffix:str
    StreetName:str
    StreetNumber:int
    StreetSuffix:str
    UnitNumber:str
    UnparsedAddress:str #les altres sense filtrar
    class Location:
        class GIS:
            Latitude:float    #SI FET
            Longitude:float   #SI FET    
class Area:
    SubdivisionName:str
class School:
    HighSchoolDistrict:list[int]
class Property:
    PropertyType:str #SI FET
class Structure:
    Basement:list[str]
    BathroomsFull:int #SI
    BathroomsHalf:int #SI
    BedroomsTotal:int #SI
    BelowGradeFinishedArea:int
    BelowGradeUnfinishedArea:int
    Cooling:list[str] #SI
    FireplacesTotal:int #SI
    GarageSpaces:int #SI
    Heating:list[str] #SI
    LivingArea:int #SI
    NewConstructionYN:bool #SI
    ParkingFeatures:list[str] 
    class Rooms:
        RoomsTotal:int #SI
    YearBuilt:int #SI
class Tax:
    Zoning:str #SI FET
class UnitTypes:
    UnitTypeType:list[str] #SI FET

llista_estils_exteriors:list[str] =  ['bungalow', 'ranch', 'art_deco', 'not_single_family', 'cape_cod', 'victorian', 'mid_century_modern', 'traditional', 'contemporary', 'craftsman', 'manufactured__mobile', 'no_distinct_style', 'italianate', 'split_level', 'american_foursquare', 'modern_farmhouse', 'neoclassical__greek', 'prairie', 'french_country', 'shingle', 'mediterranean__spanish', 'tudor', 'raised_ranch', 'garrison', 'dutch_colonial', 'a_frame', 'obstructed_view', 'colonial', 'chalet__cabin', 'georgian', 'shotgun', 'unfinished', 'farmhouse', 'geodesic_dome', 'pueblo_revival', 'log', 'raised_beach_house', 'second_empire', 'pan_asian', 'oriental', 'berm']
llista_stories:list[str] = ['1_story', '1.5_stories', '2_stories', '2.5_stories', '3_stories_or_more']    
llista_ciutats:list[str] = ['morrison', 'highland park', 'chicago', 'wilmington', 'maple park', 'big rock', 'carol stream', 'round lake beach', 'beach park', 'watseka', 'maywood', 'rantoul', 'crystal lake', 'lockport', 'tuscola', 'skokie', 'dixon', 'woodstock', 'palatine', 'hinckley', 'dekalb', 'harvard', 'aurora', 'fox', 'arlington', 'heights', 'plainfield', 'wheaton', 'buffalo', 'grove', 'river', 'oswego', 'berwyn', 'itasca', 'braidwood', 'brookfield', 'riverdale', 'oak', 'east', 'moline', 'yorkville', 'hanover', 'kildeer', 'morton', 'des', 'plaines', 'barrington', 'morris', 'mark', 'poplar', 'hampshire', 'dwight', 'mt.', 'carroll', 'granville', 'waukegan', 'burr', 'ridge', 'rockford', 'winnetka', 'cicero', 'bull', 'valley', 'naperville', 'dixmoor', 'mettawa', 'northbrook', 'bloomington', 'joliet', 'sleepy', 'hollow', 'frankfort', 'lanark', 'princeton', 'stockton', 'woodridge', 'prophetstown', 'capron', 'glen', 'ellyn', 'mchenry', 'lemont', 'sterling', 'st.', 'charles', 'orland', 'wonder', 'la', 'grange', 'long', 'zurich', 'mazon', 'glenview', 'hickory', 'hills', 'wheeling', 'lansing', 'urbana', 'hinsdale', 'countryside', 'savoy', 'glencoe', 'herscher', 'mokena', 'richmond', 'greenwood', 'evanston', 'utica', 'wauconda', 'belvidere', 'south', 'melrose', 'western', 'springs', 'midlothian', 'in', 'the', 'thornton', 'elgin', 'vernon', 'johnsburg', 'ottawa', 'lasalle', 'markham', 'normal', 'lexington', 'wadsworth', 'spring', 'weldon', 'downers', 'millington', 'tinley', 'westmont', 'grayslake', 'new', 'lenox', 'minooka', 'homewood', 'batavia', 'streator', 'genoa', 'rochelle', 'freeport', 'libertyville', 'elmhurst', 'roselle', 'burbank', 'manville', 'clinton', 'willow', 'crete', 'lawn', 'crestwood', 'calumet', 'round', 'zion', 'danville', 'burlington', 'coal', 'country', 'club', 'inverness', 'savanna', 'villa', 'avon', 'dolton', 'sheridan', 'sycamore', 'paxton', 'forest', 'sheffield', 'niles', 'harvey', 'franklin', 'gurnee', 'champaign', 'huntley', 'mundelein', 'mahomet', 'marseilles', 'hillside', 'bourbonnais', 'chadwick', 'alsip', 'effingham', 'oakland', 'decatur', 'newton', 'charleston', 'pana', 'teutopolis', 'mattoon', 'oakwood', 'warrensburg', 'robinson', 'catlin', 'tilton', 'greenup', 'homer', 'hazel', 'crest', 'holland', 'sandwich', 'piper', 'west', 'lincolnwood', 'kankakee', 'brook', 'dundee', 'matteson', 'antioch', 'ogden', 'gilman', 'neponset', 'shelbyville', 'hoopeston', 'loves', 'hutsonville', 'findlay', 'carlock', 'oregon', 'bradford', 'oglesby', 'ludlow', 'bellwood', 'richton', 'paris', 'hometown', 'palos', 'flossmoor', 'shorewood', 'flat', 'mount', 'prospect', 'addison', 'lincolnshire', 'geneva', 'north', 'sauk', 'village', 'iroquois', 'riverside', 'vandalia', 'wenona', 'elmo', 'flanagan', 'cullom', 'varna', 'lindenhurst', 'atwood', 'grant', 'beecher', 'momence', 'pembroke', 'twp', 'putnam', 'nottingham', 'elburn', 'loda', 'hawthorn', 'woods', 'justice', 'martinton', 'onarga', 'bensenville', 'steger', 'milford', 'roscoe', 'schiller', 'lynwood', 'glenwood', 'montgomery', 'paw', 'clarendon', 'ingleside', 'bolingbrook', 'algonquin', 'westchester', 'cissna', 'fisher', 'heyworth', 'pontiac', 'buckley', 'darien', 'chebanse', 'davis', 'junction', 'neoga', 'farmer', 'cortland', 'bluff', 'seneca', 'peru', 'carpentersville', 'bloomingdale', 'gilberts', 'monee', 'winfield', 'elmwood', 'shannon', 'custer', 'wilmette', 'hill', 'glendale', 'reddick', 'saybrook', 'strasburg', 'sugar', 'eleroy', 'assumption', 'newark', 'bartlett', 'evergreen', 'arcola', 'channahon', 'wood', 'dale', 'bridgeview', 'dell', 'marengo', 'colfax', 'island', 'kirkland', 'falls', 'donovan', 'ancona', 'tiskilwa', 'blue', 'schaumburg', 'university', 'marshall', 'hoffman', 'estates', 'holiday', 'sheldon', 'brownstown', 'westville', 'deerfield', 'gibson', 'norridge', 'ladd', 'tower', 'plano', 'stone', 'burnham', 'summit', 'sullivan', 'northlake', 'phoenix', 'thomasboro', 'broadview', 'forsyth', 'roanoke', 'lawndale', 'berkeley', 'somonauk', 'streamwood', 'medinah', 'amboy', 'durand', 'leland', 'apple', 'herrick', 'lombard', 'manhattan', 'confidential', 'lena', 'bannockburn', 'riverwoods', 'beaverville', 'ashkum', 'cary', 'robbins', 'galena', 'campton', 'wayne', 'monticello', 'olympia', 'fields', 'ohio', 'esmond', 'green', 'oaks', 'posen', 'willowbrook', 'compton', 'leroy', 'chrisman', 'hammond', 'worth', 'farina', 'winnebago', 'wellington', 'northfield', 'georgetown', 'polo', 'carlyle', 'walnut', 'cherry', 'peoria', 'bedford', 'harwood', 'lakemoor', 'mclean', 'steward', 'rossville', 'windsor', 'romeoville', 'orangeville', 'ashton', 'ivanhoe', 'westervelt', 'beloit', 'white', 'heath', 'lisle', 'bradley', 'fithian', 'warrenville', 'caledonia', 'kewanee', 'union', 'odell', 'pingree', 'lyons', 'tonica', 'earlville', 'moweaqua', 'elwood', 'kansas', 'casey', 'wapella', 'foosland', 'stickney', 'tolono', 'pekin', 'peotone', 'anne', 'deer', 'milledgeville', 'rolling', 'meadows', 'olney', 'lakewood', 'volo', 'delavan', 'clifton', 'chenoa', 'minonk', 'malta', 'machesney', 'indian', 'head', 'lerna', 'lacon', 'columbia', 'virgil', 'wataga', 'fulton', 'ridgefarm', 'stillman', 'rockdale', 'hudson', 'maroa', 'mendota', 'hainesville', 'kingston', 'metcalf', 'hebron', 'downs', 'silvis', 'mackinaw', 'warren', 'hume', 'port', 'lostant', 'elk', 'bement', 'lincoln', 'rankin', 'manteno', 'chillicothe', 'springfield', 'sadorus', 'byron', 'philo', 'scales', 'mound', 'buda', 'benson', 'fairbury', 'chatsworth', 'winthrop', 'harbor', 'potomac', 'shabbona', 'groveland', 'forreston', 'kenilworth', 'highwood', 'bonfield', 'ellsworth', 'cropsey', 'hopedale', 'oblong', 'atkinson', 'diamond', 'toluca', 'claytonville', 'gifford', 'stewardson', 'dover', 'el', 'paso', 'minier', 'joseph', 'rockton', 'washington', 'merrionette', 'eola', 'oakbrook', 'terrace', 'mansfield', 'taylorville', 'braceville', 'atlanta', 'ford', 'macon', 'forrest', 'flora', 'dalton', 'henry', 'magnolia', 'verona', 'shumway', 'harpe', 'sublette', 'manito', 'cornell', 'wyanet', 'norwood', 'township', 'camargo', 'sidell', 'mcconnell', 'waterman', 'eldena', 'pecatonica', 'lakes', 'ringwood', 'niantic', 'melvin', 'wildwood', 'towanda', 'dakota', 'place', 'hindsboro', 'gridley', 'dewey', 'aroma', 'tampico', 'de', 'land', 'newman', 'garden', 'prairie', 'petersburg', 'bristol', 'stonington', 'hennepin', 'boody', 'martinsville', 'broadwell', 'argenta', 'blackstone', 'brocton', 'bismarck', 'mason', 'sidney', 'danvers', 'ina', 'plymouth', 'lovington', 'fairmount', 'creek', 'third', 'summerset', 'cerro', 'gordo', 'eureka', 'lamoille', 'oreana', 'alvin', 'laplace', 'rutland', 'cooksville', 'crescent', 'stanford', 'kings', 'vermillion', 'seymour', 'serena', 'bethany', 'xenia', 'homes', 'gages', 'pesotum', 'naplate', 'manlius', 'mcnabb', 'cedarville', 'arthur', 'trout', 'armington', 'view', 'anchor', 'cottage', 'westfield', 'chana', 'rosemont', 'winslow', 'essex', 'broadlands', 'mccullom', 'girard', 'hodgkins', 'wheeler', 'liberty', 'cabery', 'lewistown', 'thomson', 'shirley', 'monroe', 'center', 'lee', 'goodfield', 'altamont', 'lyndon', 'cisco', 'buckingham', 'belleville', 'ransom', 'montrose', 'ridott', 'sparland', 'illiopolis', 'mccook', 'waynesville', 'depue', 'cahokia', 'shobonier', 'palestine', 'secor', 'dieterich', 'bellflower', 'allerton', 'dalzell', 'humboldt', 'hidalgo', 'murphysboro', 'gardner', 'highlands', 'pearl', 'tremont', 'emington', 'harmon', 'graymont', 'brooklyn', 'penfield', 'arrowsmith', 'creve', 'coeur', 'thawville', 'cedar', 'point', 'saunemin', 'roberts', 'canton', 'grand', 'watson', 'henning', 'woodland', 'leaf', 'congerville', 'elizabeth', 'erie', 'middletown', 'ellisville', 'warsaw', 'easton', 'annawan', 'pulaski', 'metamora', 'godley', 'edgewood', 'dennison', 'elliott', 'saint', 'allenville', 'kappa', 'royal', 'toledo', 'peter', 'ivesdale', 'ashmore', 'bondville', 'morrisonville', 'jewett', 'nora', 'edwardsville', 'omaha', 'bureau', 'harristown', 'chatham', 'armstrong', 'albany', 'sibley', 'clare', 'nokomis', 'forestview', 'oakley', 'dewitt', 'kenney', 'creston', 'athens', 'geneseo', 'centralia', 'kinsman', 'madison', 'millbrook', 'greenview', 'germantown', 'annapolis', 'millford', 'cowden', 'alton', 'gays', 'virden', 'leyden', 'seward', 'litchfield', 'kinmundy', 'cofidential', 'woodhull', 'maquon', 'danforth', 'edwards', 'david', 'chemung', 'fairview', 'woosung', 'ohlman', 'lawrenceville', 'seatonville', 'glasford', 'galva', 'campus', 'mascoutah', 'german', 'mode', 'oconee', 'kasbeer', 'louisville', 'golf', 'jacksonville', 'kempton', 'hamilton', 'carmel', 'sumner', 'camp', 'rosamond', 'trilla', 'old', 'mill', 'lindenwood', 'leonore', 'collinsville', 'malden', 'nelson', 'salem', 'alma', 'baileyville', 'coulterville', 'elwin', 'dana', 'galesburg', 'washburn', 'ofallon', 'chestnut', 'clarence', 'quincy', 'harmony', 'carbon', 'indianola', 'pocahontas', 'gorham', 'broughton', 'beason', 'holcomb', 'muncie', 'san', 'jose', 'jerseyville', 'holder', 'jeffersonville', 'granite', 'witt']    
llista_counties:list[str] = ['whiteside', 'lake', 'cook', 'will', 'kane', 'du', 'page', 'iroquois', 'champaign', 'mc', 'henry', 'douglas', 'lee', 'de', 'kalb', 'dekalb', 'mchenry', 'kendall', 'rock', 'island', 'grundy', 'putnam', 'boone', 'livingston', 'carroll', 'winnebago', 'lean', 'bureau', 'jo', 'daviess', 'kankakee', 'lasalle', 'la', 'salle', 'mclean', 'witt', 'ogle', 'stephenson', 'vermilion', 'warren', 'ford', 'effingham', 'coles', 'macon', 'jasper', 'christian', 'crawford', 'shelby', 'cumberland', 'dupage', 'stark', 'edgar', 'fayette', 'marshall', 'piatt', 'clark', 'moultrie', 'woodford', 'other', 'peoria', 'mason', 'tazewell', 'richland', 'monroe', 'knox', 'logan', 'sangamon', 'clay', 'hancock', 'menard', 'jefferson', 'madison', 'macoupin', 'fulton', 'st.', 'clair', 'saint', 'jackson', 'dewitt', 'gallatin', 'montgomery', 'marion', 'lawrence', 'adams', 'hamilton', 'jersey']
llista_estats:list[str] = ["IL"]
llista_zoning_types:list[str] = ['commr', 'agric', 'offic', 'multi', 'rtail', 'other', 'pmd', 'indus', 'singl', 'manuf', 'pud', 'wrhse', 'lnc']
llista_tipus_propietats:list[str] = ['commercial', 'sale', 'residential', 'farm', 'income', 'business', 'opportunity', 'lease', 'manufactured', 'in', 'park']
llista_heatings:list[str] = ['natural gas', 'forced air', 'heat pump', 'radiant', 'steam', 'radiator/s', 'natural', 'gas', 'other']
llista_coolings:list[str] = ['central air', 'zoned', 'central individual', 'none', 'office only', 'partial', 'window/wall units', 'reverse cycle', 'other']
def main():
    st.set_page_config(layout="wide")

    st.header("Welcome to our Algorithm!")
    st.subheader("By inputing the basic data of your real estate, we will predict the price")
    st.markdown(
        """
        <style>
        .center-bold {
            text-align: center;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

#ListingID i containers de coordenades
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1], vertical_alignment="center")
    with c1:
        st.markdown('<div class="center-bold">House Information</', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="center-bold">House Situation</', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="center-bold">Building Details</', unsafe_allow_html=True)
    with c4:
        try:
            Listing.Location.GIS.Latitude = float(st.text_input("Latitude", "42.0071")) 
        except:
            st.text("Input a valid latitude")
    with c5:   
        try:
            Listing.Location.GIS.Longitude = float(st.text_input("Longitude", "2.0310"))    
        except:
            st.text("Input a valid longitude")
        
    #Layout    
    a1, a2 = st.columns([3, 2])
    #MEITAT ESQUERRA
    with a1:
        with st.container(height=660, border=True):
            c1, c2, c3= st.columns(3)
            with c1:
                ImageData.c1c6 = st.slider("Condition", 1.0, 6.0, 3.5, -0.1)
                ImageData.q1q6 = st.slider("Quality", 1.0, 6.0, 3.5, -0.1)
                ImageData.style.exterior = st.selectbox("Exterior Style", sorted(llista_estils_exteriors))               
                ImageData.style.stories = st.selectbox("Interior Style", sorted(llista_stories)) 
                Property.PropertyType = st.selectbox("Property Type", sorted(llista_tipus_propietats))
                Characteristics.LotSizeSquareFeet = st.number_input("Square feet", value=1)
                Structure.LivingArea = st.number_input("Living area", value=1)               
            with c2:
                Listing.City = st.selectbox("City", sorted(llista_ciutats))
                Listing.PostalCode = int(st.text_input("Postal Code", "60000"))
                Listing.CountyOrParish = st.selectbox("County or Parish", sorted(llista_counties))
                Listing.StateOrProvince = st.selectbox("State or Province", sorted(llista_estats))
                Tax.Zoning = st.selectbox("Tax Zoning", sorted(llista_zoning_types))                
                Structure.Cooling = st.multiselect("Type of cooling", sorted(llista_coolings))
                Structure.YearBuilt = st.number_input("Year built", value=2024)
                Structure.NewConstructionYN = st.checkbox("New construction")
            with c3:
                Structure.BathroomsFull = st.number_input("Number of full bathrooms", value=1)
                Structure.BathroomsHalf = st.number_input("Number of half bathrooms", value=1)
                Structure.BedroomsTotal = st.number_input("Number of bedrooms", value=1)
                Structure.Rooms.RoomsTotal = st.number_input("Number of rooms", value=1)
                Structure.GarageSpaces = st.number_input("Number of garage spaces", value=1)
                Structure.Heating = st.multiselect("Type of Heating", sorted(llista_heatings))
                Structure.FireplacesTotal = st.number_input("Number of fireplaces", value=1)


    #MEITAT DRETA (MAPA)        
    with a2:
        with st.container(height=500, border=True):
            mapa_centrat = folium.Map(location=[Listing.Location.GIS.Latitude, Listing.Location.GIS.Longitude], zoom_start=7)
            folium.Marker(
            [Listing.Location.GIS.Latitude, Listing.Location.GIS.Longitude],
            ).add_to(mapa_centrat)
            st_folium(mapa_centrat, height = 500, width = 500)  
        Listing.ListingId = st.text_input("ListingId", "mrd123454678")
        #COSES SOTA EL MAPA
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            executa_t2 = st.button("Run Algorithm", type="primary")       

    vector_parametres = ['Characteristics.LotFeatures', 'Characteristics.LotSizeSquareFeet', 'ImageData.c1c6.summary.bathroom', 'ImageData.c1c6.summary.exterior', 'ImageData.c1c6.summary.interior', 'ImageData.c1c6.summary.kitchen', 'ImageData.c1c6.summary.property', 'ImageData.features_reso.results', 'ImageData.q1q6.summary.bathroom', 'ImageData.q1q6.summary.exterior', 'ImageData.q1q6.summary.interior', 'ImageData.q1q6.summary.kitchen', 'ImageData.q1q6.summary.property', 'ImageData.room_type_reso.results', 'ImageData.style.exterior.summary.label', 'ImageData.style.stories.summary.label', 'Listing.Dates.CloseDate', 'Listing.ListingId', 'Location.Address.CensusBlock', 'Location.Address.CensusTract', 'Location.Address.City', 'Location.Address.CountyOrParish', 'Location.Address.PostalCode', 'Location.Address.PostalCodePlus4', 'Location.Address.StateOrProvince', 'Location.Address.StreetDirectionPrefix', 'Location.Address.StreetDirectionSuffix', 'Location.Address.StreetName', 'Location.Address.StreetNumber', 'Location.Address.StreetSuffix', 'Location.Address.UnitNumber', 'Location.Address.UnparsedAddress', 'Location.Area.SubdivisionName', 'Location.GIS.Latitude', 'Location.GIS.Longitude', 'Location.School.HighSchoolDistrict', 'Property.PropertyType', 'Structure.Basement', 'Structure.BathroomsFull', 'Structure.BathroomsHalf', 'Structure.BedroomsTotal', 'Structure.BelowGradeFinishedArea', 'Structure.BelowGradeUnfinishedArea', 'Structure.Cooling', 'Structure.FireplacesTotal', 'Structure.GarageSpaces', 'Structure.Heating', 'Structure.LivingArea', 'Structure.NewConstructionYN', 'Structure.ParkingFeatures', 'Structure.Rooms.RoomsTotal', 'Structure.YearBuilt', 'Tax.Zoning', 'UnitTypes.UnitTypeType']
    vector_valors = ["", Characteristics.LotSizeSquareFeet, "", "", "", "", ImageData.c1c6, "", "", "", "", "", ImageData.q1q6, "", ImageData.style.exterior, ImageData.style.stories, "", Listing.ListingId, "", "", Listing.City, Listing.CountyOrParish, Listing.PostalCode, "", Listing.StateOrProvince, "", "", "", "", "", "", "", "", Listing.Location.GIS.Latitude, Listing.Location.GIS.Longitude, "", Property.PropertyType, "", Structure.BathroomsFull, Structure.BathroomsHalf, Structure.BedroomsTotal, "", "", Structure.Cooling, Structure.FireplacesTotal, Structure.GarageSpaces, Structure.Heating, Structure.LivingArea, Structure.NewConstructionYN, "", Structure.Rooms.RoomsTotal, Structure.YearBuilt, Tax.Zoning, ""]
   
    #Clicat el botó, exporta els valors, calcula el preu i el displayeja
    if executa_t2: 
        #ESCRIU VALORS
        with open("valors_casa.csv", mode="w", newline="") as excel_valors:
            writer = csv.writer(excel_valors)
            
            writer.writerow(vector_parametres)
            writer.writerow(vector_valors)

        t2_demo.main()

        #LLEGEIX EL PREU I EL DISPLAYEJA
        with open("output.txt", "r") as text:       
            
            preu:list[str] = ["$", text.read()]

        st.title(''.join(preu))    


main()