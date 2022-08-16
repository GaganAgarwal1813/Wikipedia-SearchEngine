import re
from nltk.corpus import stopwords
from Stemmer import Stemmer

stop_words = set(stopwords.words('english')) 
stemmer = Stemmer('porter')


def tokenize(text):
    text = re.split(r'[^A-Za-z0-9]+', text)
    tokens = []
    for line in text:
        word = stemmer.stemWord(line)
        if len(word) > 2 and len(word) < 20 and word not in stop_words:
            tokens.append(word)
    return tokens
    
    
def extractLinks(text):
    links = {}
    raw = text.split("\n")
    for lines in raw:
        if lines and lines[0] == '*':
            line = tokenize(lines)
            for i in line:
            	if i in links:
            		links[i] +=1
            	else:
            		links[i] = 1        	
    return links 


def getInfobox(text):
    cont = text.split("{{infobox")
    info = []
    if len(cont) <= 1:
        return {}
    flag= False
    for infob in cont:
        traw = infob.split("\n")
        if (not flag):
            flag=True
        else :
            for lines in traw:
                if lines == "}}":
                    break
                info += tokenize(lines)
    d = {}
    for i in info:
    	if i in d:
    		d[i] = d[i]+1
    	else:
    		d[i] = 1
    return d


def getReferences(text):
    ref = text.split("[[")
    ref = tokenize(ref[0])
    d = {}
    for i in ref:
    	if i in d:
    		d[i] +=1
    	else:
    		d[i] = 1
    return d



def extractCategories(text):
    cat = text.split("[[category:")
    cat = cat[1:]
    d = {}
    for line in cat:
    	words = tokenize(line)
    	for i in words:
    		if i in d:
    			d[i] = d[i]+1
    		else:
    			d[i] = 1
    return d

def refandextType(name):
	l = []
	l.append("==" + name + "==")
	l.append("== " + name + "==")		
	l.append("==" + name + " ==")		
	l.append("== " + name + " ==")		
	return l
	

def processContent(text):
    text=text.lower()
    references={}
    links={}
    categories={}
    ref = refandextType("references")
    ext = refandextType("external links")
    data=text.split(ref[0])
    if data[0] == text:
        data= text.split(ref[1])
    if data[0]==text:
        data= text.split(ref[2])
    if data[0]==text:
        data= text.split(ref[3])
    if len(data)==1:

        categories = extractCategories(data[0])

        haslink=1
        catdata=data[0].split(ext[0])
        if len(catdata)==1:
            catdata=data[0].split(ext[1])
        if len(catdata)==1:
            catdata=data[0].split(ext[2])
        if len(catdata)==1:
            catdata=data[0].split(ext[3])
        if len(catdata)==1:
            links={}
            haslink=0
        if (haslink):
            links=extractLinks(catdata[1])
    else:
        haslink=1
        catdata=data[1].split(ext[0])
        if len(catdata)==1:
            catdata=data[1].split(ext[1])
        if len(catdata)==1:
            catdata=data[1].split(ext[2])
        if len(catdata)==1:
            catdata=data[1].split(ext[3])
        if len(catdata)==1:
            links={}
            haslink=0
        if (haslink):
            links = extractLinks(catdata[1])
        
        references = getReferences(data[1])
        categories = extractCategories(data[1])
 
    infobox= getInfobox(data[0])
    body = tokenize(data[0])
    d = {}
    for i in body:
    	if i in d:
    		d[i] = d[i]+1
    	else:
    		d[i] = 1
    return d, references, categories, links, infobox    
   
text = "{{Infobox WorldScouting |name=Pushmataha Area Council |image=Pushmataha Area Council CSP.png |type=council |owner=[[Boy Scouts of America]] |headquarters=[[Columbus, Mississippi]] |location= |country=United States |coords= |f-date= 1925 |defunct= |founder= |members= |chiefscouttitle=Scout Executive |chiefscout=Keith Walton |chiefscouttitle2=Council President |chiefscout2=Tripp Hairston |chiefscouttitle3= |chiefscout3= |website =http://www.pushmataha.org/ }} The '''Pushmataha Area Council''' is part of the [[Boy Scouts of America]]. It renders service to Scout units in ten counties of North [[Mississippi]], providing skills training and character development to boys and girls between the ages of 5 and 18. The council also serves boys and girls between the ages of 14 and 21 through [[Venturing]] Crews and Explorer posts. In 2007, 24 [[Eagle Scout (Boy Scouts of America)|Eagle Scout]] ranks were earned in the Pushmataha Area Council, and 20 Scouts earned the God and Country Award. ==History== [[Image:StatueOfLibertyColumbus2.jpg|thumb|upright|Columbus, Mississippi]] The Pushmataha Area Council was established by the Boy Scouts of America in June, 1925. The council was originally named the East Mississippi Council, but this name was changed in 1929 to honor Chief [[Pushmataha]] of the [[Choctaw]] tribe. Chief Pushmataha once told a group of chiefs that he was not born, but instead stepped, full grown and dressed for battle, from the split in a tree that had been struck by lightning. This story has been incorporated into the Pushmataha Area Council Shoulder Patch shown above. The patch shows a full-grown Pushmataha emerging from a tree struck by lightning. Camp Seminole has a sign on its grounds noting the tree from which Pushmataha supposedly appeared. In 1925, the headquarters of the council was in [[West Point, Mississippi]], on Main Street. In 1960s, the council office was moved to its current location at 420 31st Avenue North, [[Columbus, Mississippi]]. The Pushmataha Area Council is one of the smallest Boy Scout councils in America. It is not unusual for other councils to have districts larger than the entire Pushmataha Area Council. In 1950, the council erected a miniature [[Statue of Liberty]] in the middle of downtown Columbus, Mississippi, as part of a national effort in the Boy Scouts to erect 200 of these statues. Fewer than 100 of these statues still exist, and even fewer exist intact. The Pushmataha Area Council statue is one of the few intact ones that exist today. When fully staffed with professionals, the Pushmataha Area Council has a Scout Executive, two District Executives, and a full-time Camp Ranger. One District Executive resigned in 2007, and the Executive Board of the council did not hire a replacement for the position. The Camp Ranger resigned in the spring of 2009, and the camp is currently (2010) served by a part-time, volunteer, interim Camp Ranger. The second District Executive resigned in the early fall of 2009, and the council Executive Board did not hire anyone fill that position. The Scout Executive announced in November, 2009 that he was resigning, and as of April, 2010, the Scout Executive position is still vacant. The BSA Regional Director is acting as the official Scout Executive for the council until one is hired. The Regional Director is in another state, and is not present to oversee day-to-day operations of the council. The council is being operated by a small corps of volunteers, and the 2010 FOS campaigns are being run by volunteers with no professional guidance or assistance. The Council President, George Purnell, has been in office for six years. All previous council presidents (1925–2004) served a maximum of three years. ==Districts== When the council began, each town with a Scout troop was its own District. For example, troops in [[Columbus, Mississippi]] were in the Columbus District. Later the council evolved into having three districts, the Running Bear District, the Talking Warrior District, and the Tombigbee District. In 1990s, these three districts were reorganized to create two new districts, the Choctaw District and the Chickasaw District. The Choctaw District covers five counties: Clay, Lowndes, Oktibbeha, Webster, and Noxubee. The Chickasaw District also covers five counties: Monroe, Winston, Chickasaw, Choctaw, and Calhoun. ==Events== The Pushmataha Area Council hosts numerous events each year. These include: * Eagle Recognition Banquet (early spring) * Council Pinewood Derby (spring) * Summer Camp (June) * Cub Scout Day Camp (June) * [[Webelos]] Resident Camp (June) * [[Cub Scouting (Boy Scouts of America)|Cub Scout]] Leader Specific Training (September&nbsp;— March) * [[Boy Scout]] Leader Training (late fall) * [[Wood Badge (Boy Scouts of America)|Wood Badge]] Training (bi-annually) * MSU Scout Football Day (fall) * MSU Scout Baseball Day (spring) * [[Cub Scouting (Boy Scouts of America)|Cub Scout]] Family Weekend (semi-annually) * Tiger Leader Training (fall) ==Funding== The Pushmataha Area Council is funded by donations made by civic organizations, businesses, and individuals. Several different [[United Way of America|United Way]] groups contribute to the council, and most United way funding has remained strong. United way of Oktibbeha County is an exception, as they have cut their funding to the council by over half in recent years. The Pushmataha Area Council is a 501(c) non-profit organization. ==Service== Through the [[Cub Scouting (Boy Scouts of America)|Cub Scouting]], [[Boy Scouting (Boy Scouts of America)|Boy Scouting]], and [[Venturing (Boy Scouts of America)|Venturing]] programs, the Pushmataha Area Council serves youth ages 6 through 21. The council offers [[Learning for Life]], a character education program used by local schools. Explorer posts in the council offer vocation-oriented experience to teenage boys and girls in the council's ten county area. ==Camp Seminole== {{Infobox WorldScouting |name=Camp Seminole |image=Camp Seminole.png |type=camp |location=[[Starkville, Mississippi]] |coords= |f-date= 1982 |defunct= |founders= |founder= |members= |chiefscouttitle=Camp Ranger |chiefscout= |chiefscouttitle2= |chiefscout2= |chiefscouttitle3= |chiefscout3= |website=http://CampSeminole.org/ |portal=no }} The original council camp was Camp Pine Springs, in Monroe County, located along the Buttahatchie River north of Columbus, Mississippi. Camp Palila, located in [[Louisville, Mississippi]], became the council camp in 1953. Camp Palila served as the council camp for thirty years prior to 1980. The state of Mississippi had leased the land to the council, but the legislature failed to complete the new lease before the original lease ended. The land used for Camp Palila reverted to control of the state, and is now Legion State Park. The current council camp for the Pushmataha Area Council is Camp Seminole, about five miles north of [[Starkville, Mississippi]]. Camp Seminole hosts, among other activities, council [[summer camps]], [[Cub Scouting (Boy Scouts of America)|Cub Scout]] campouts, leadership training sessions, [[Wood Badge (Boy Scouts of America)|Wood Badge]] courses, and [[Order of the Arrow]] events. Camp Seminole was named for Seminole Manufacturing of Columbus, Mississippi, which donated significant financial support toward the camp's construction. ===History=== Camp Seminole was built on {{convert|285|acre|km2}} of land purchased by the Pushmataha Area Council in 1982. The need for building the camp came about when the lease on the previous council camp (Camp Palila) expired, and the Mississippi legislature did not renew the lease. A Brownsea-22 training course was held on the grounds of the new camp in 1982, before any structures or other improvements had been made. Several council camporees were conducted on the grounds before Camp Seminole was fully operational. In June 1986, Camp Seminole was declared officially open when the Pushmataha Area Council [[summer camp]] was held there for the first time. ===Facilities=== Camp Seminole has a dining hall that seats 200 people, a {{convert|12|acre|m2|sing=on}} lake, nine camp sites, a [[C.O.P.E.]] Lodge, an activity field, a shooting sports arena, an [[obstacle course]], numerous open shelters, an environmental center, the [[Chakchiuma]] Nature Trail, a trading post, and the Nita Chito Scout Museum. Roads on the camp are mainly of red clay gravel construction. ===Activities=== Camp Seminole is primarily a [[Boy Scout]] camp, and is used for camporees, summer camps, Scout leader training, [[Cub Scouting (Boy Scouts of America)|Cub Scout]] campouts, and other Boy scout related events. The camp is also used to house [[Habitat for Humanity]] volunteers, for land navigation training by local [[National Guard (United States)|National Guard]] and [[R.O.T.C.]] units, for Mississippi Hunter Safety Education Training, for [[Red Cross]] [[CPR]] and [[First Aid]] Training sessions, and other community and civic events. ===Topography=== The grounds of Camp Seminole average {{convert|230|ft|m}} above sea level. ===Climate=== The climate at Camp Seminole is considered temperate. Winter temperatures rarely drop below freezing, and summer temperatures reach their peak in July and August, when it can reach 95-100 degrees Fahrenheit (35-38 degrees Celsius). The rainy season is early December through late March. Rainfall averages 62 annually. ==Watonala Lodge== {{Infobox WorldScouting | name =Watonala Lodge | image =Watonala Lodge.png | image-size = | caption = | type = | owner = | age = | headquarters =[[Columbus, Mississippi]] | location = | country = | coords = | f-date =September, 1939 | defunct = | founders = | founder = | award-for = | members =less than 125 | chiefscouttitle =Lodge Chief | chiefscout =Daniel Grebner | chiefscouttitle2 =Lodge Adviser | chiefscout2 =Peyton Peralto | chiefscouttitle3 =Associate Lodge Adviser | chiefscout3 =Tom Holder | website =http://Watonala.org/ | affiliation = | portal=no }} The [[Order of the Arrow]] is represented by the Watonala Lodge. It supports the Scouting programs of the council through leadership, camping, and service. ===History=== On September 1, 1939, five adult [[Boy Scout]] leaders from the Pushmataha Area Council attended an [[Order of the Arrow]] Area Fellowship in [[Birmingham, Alabama]], and learned about the purpose and mission of the Order. Upon returning to the Pushmataha Area Council, an application for a charter was submitted to the National Order of the Arrow office. The initial charter was issued in the latter part of September, 1939. When the initial charter was issued, it was issued in the name of the local council, as Pushmataha Lodge. In January, 1942, Pushmataha Lodge chose its Native American name, Watonala Lodge. In the [[Choctaw language]], Watonala means white egret, or white water bird. The first lodge event was held in the Spring of 1940 at the [[Natchez Trace]] Game Preserve, near [[Houston, Mississippi]]. Lodge membership began to grow, as new [[Arrowmen]] were inducted during each council [[camporee]]. Membership slowed considerably during [[World War II]], but resumed its pre-war growth during the few years immediately following World War II. The founding of Watonala Lodge in 1939 is well documented, although there is an [[oral history]] that places the origin of the lodge ten years earlier, in 1929. ===Service=== Watonala Lodge devotes much of its service time to development and maintenance of their home camp, [[Camp Seminole (Mississippi)|Camp Seminole]], which is located five miles north of [[Starkville, Mississippi]]. The lodge also publishes an online Where To Go Camping Guide at www.Watonala.Org, aimed at helping other Boy Scouts and the general public find good places to camp, canoe, and hike. ===Memorabilia=== The dominant theme of most Watonala patches and memorabilia is its [[totem]], the white egret. The totem is usually shown in profile, facing the viewers left, and headed upward in flight. There are numerous variations of this design, with the totem image varying slightly with each new patch issue. The lodge issues a new lodge flap every two or three years, and sometimes issues specific patches for OA events, such as [[Conclave]], National Order of the Arrow Conference ([[Order of the arrow#National Order of the Arrow Conference|NOAC]] ), and service events. Compared to many OA lodges, Watonala Lodge has always been comparatively small in membership numbers. This is due largely to being in a rural council having only ten counties. Because of smaller membership, the quantity of Watonala memorabilia available is usually smaller than most OA lodges. ==See also== *[[Scouting in Mississippi]] *[[Replicas of the Statue of Liberty]] ==References== {{reflist}} *[http://www.watonala.org Watonala Lodge Home Page] *[http://www.pushmataha.org/watonala/phpBB2/index.php Watonalas Where To Go Camping Guide] *[http://www.pushmataha.org/watonala/history/documented_origin.htm Watonala Documented History] *[http://www.Pushmataha.org Pushmataha Area Council] * Unbound manuscripts, Nita Chito Scout Museum * ''Scouting In Oktibbeha County'', unpublished manuscript [[Category:Local councils of the Boy Scouts of America]] [[Category:Southern Region (Boy Scouts of America)]] [[Category:Youth organizations based in Mississippi]] [[Category:1925 establishments in Mississippi]]"

#body, references, categories, links, infobox = processContent(text)
#print("Body : ", body)
#print("Infobox : ", infobox)
#print("links : ", links)
#print("References : ", references)
#print("Categories : ", categories)




