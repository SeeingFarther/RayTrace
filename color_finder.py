import numpy as np
import random
from light import Light
from material import Material
from scene_settings import SceneSettings
from ray import Ray
from surfaces.cube import Cube
from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere
from surfaces.triangle import Triangle
from utilities import *


class ColorFinder:
    def __init__(self, scene_settings, lights, surfaces, materials, background_color):
        self.scene_settings = scene_settings
        self.lights = lights
        self.surfaces = surfaces
        self.materials = materials
        self.background_color = background_color

        # Prevents black spots
        self.black_spots_factor = 0.0002

        # Seed for random (used sha256 for creating seed like in random default)
        seed = 14280006676694483034534173907049361154901655061976288708835305050063282117760217571340348756809211045946011625065076636394079994214476889255519655877148309062066683415803566907076619704109492325101374443069101241667267580542904208188732003971688851097322755056195963681108434118812922381115557264786896278376727771222442427554715329462625616863757150623450409685005513582510651927546639632599575420367666993985798407260398988088451948367855333113049665497352908703471879339909841933905522450261636476268601216853655753185216875411541516840927124506804799376832544992757527963818665818101374645222034223409553556574994763847306061275678921404564693835063673274134041339571933707884761736616338588791311181951174088877338943994679985652178661138795213018187528876890356033569325973061615431175845254239640314761440761263949801969389145286297036623668840054625180091114805519438273402381662896607424993103807014167170497126558943916400475155796386369637271577316042803020952662601105411423316773707757464669209236220644061368721769948990680054478856628445234943538052608833535878375081808055696637171077857854560673948594381453800731352357254988651618848578081671379998169006850692632528562232342573885778707472066543494433510832047330235670721338545553510590706308530849659589495383808653581876110003199710381353735729166205176234719379268920970162009530468664027597084748151313199230620415735217626129019357226938881191792018965941444326916350408629771214897655339250856821454902628665937390687688813967974863156246997149965128971178035821431057997047237897723924730411543338794550744858781875744801246045767277067824798549444319295500162500938617473527488013888949740223547680862752797104821535546774020461845887607630637624298657198568070885998529704460456805823363969068506083779347653673001729038563996319689655133531739110838381090228838798610819792953970698911817641043462331664105850391880885742426523296921392517959483119584999478332558655286383828001266596515544998759410717385818784673006152963410095504055367001970922337635763547285847684751416853789911520204186796380313260135417889028623337260954588964380724485560644398089188301718474826732947361475079326274060948790582096819431228533896432741534350746631577662644013350257456204611664760729047245723094030995076065136606497175152488429123379389280461643128462533404863503628946206505685693781073241222197586475902016312649552034323886006616587580584205580658312411664493921705329317061432201950268416679093388398385235553122611898728229347662871955569003621616076526952368007756819906380044546048430672401066231134387123309661574617807424384522649524252950681891334809092876711955841081337804803588711224754315078514826530958141739121426944640632499337219568525429137036380128059738099784116707930037615225125631651681199285476938069578507124277175545777040239227443898949709271456192566884742208814947177645339841917593071117073603434717196890752019535476627324139411866878059058694181032508760797710761509796160441637181867692548925303689122159598829596954170264001535908540248190808158224926112854766629140689775731083884204188635036922825954328684404125715299512111442917754721081407565008264374041008334940082720711349158433667230223562536698752568728948135919776262018551457566806584824340498732189643300847842130246311174023903008490393948469243392915875608424932842661621649843734626757162485632624489957409168035109278707764614322511969388363585168269739603888728867913843528510463932591017947755870873393242679685110462694029186720647784521059779242450322013427501008868726053228401584931191260467355275197845456440082052620969237842164127812434924714585906221470331905851799722453934569829722464163060714478302058623575109526841019416271207558075820766130826680274601132545716983834880429036483268218843815479478545261064502633481412198544148391514277713181375996298262425250382727000356305766413436885136634646235723009043621290997174033303124837105213218033303428956117096838132480271521937776134251483102184808129329073244939104855214344514445167329930193313497241141639679081131959713440669023360298732341278784908939253435794523511081694201119397717075139399388672060781797821616206626160270100568066757307835717622641040528163846555516035426576789104264179395784755863692738963359025344479472981149726902504403298693823685699222741703212811045784997695204100438414784624954380732357573834798069562513616265681402715654695583685746307884502239069261156975644962311257139309551214152003089771080988952479702199994769730054250109130219177721192522802668638882085449010509322426200168976003945669831878277143005639699372058840235731334918628626457881081372249170318715011568451382244993006315658983915572649920043978303630589633910174056259224366730706390126966814885222798614212469233153712521183335987333945961780844315743970032801772485130276208686631902844217659147440229209554574798471137258802316321834425422726242444932828532621412136179644070863566943179177190168184433527617188551700091122584134063874413539623123175874592765986497689492231893918472223587067902756126635713227614056725150523375863100925056389759373835362916323855141029035021924072969169286943465217850310803017825891767662268661338511782456291993138916524558348824681821594917289676464751707212772341565014541217376942551585121650141152139448139671798024574739729262829802454641169493706044106661053019510133599986710538152875709979699787366900279689941128493815788338700577006574546085504620033584670636678688862925322124525161667853379062817896930746026816713388798174490144957578728421333031586890763782044587344589886012714027130859459221446650519668785794262535295875043575619787114409002730146256626345421016483447293928743477110019682107258706448891713907736404560253165338180096601152365455811169396545120870040477052358639691778305110092298983326160788083490778493420312078470656200309769890102919269000734572058491209843779344950872613783829573615325835450364831589928404689949595425472002561946488009378318279872043817482293390181236275271294936443920941
        random.seed(seed)

    # Get and set functions
    def getSceneSettings(self):
        return self.scene_settings

    def getLights(self):
        return self.lights

    def getSurfaces(self):
        return self.surfaces

    def getMaterials(self):
        return self.materials

    def getBackgroundColor(self):
        return self.background_color

    def setSceneSettings(self, scene_settings):
        self.scene_settings = scene_settings

    def setLights(self, lights):
        self.lights = lights

    def setSurfaces(self, surfaces):
        self.surfaces = surfaces

    def setMaterials(self, materials):
        self.materials = materials

    def setBackgroundColor(self, background_color):
        self.background_color = background_color

    def calculateRaysPrecentage(self, ray, light, N, surface):
        # Find plane
        # N · P + d = 0 => d = - N · P
        N = normalize(N)
        light_position = light.getPosition()
        distance = -light_position.dot(N)

        # Find where point with coordinates x = 1, y = 1 on plane using z =  - (Ax + By + D) / C
        z = -(N[0] + N[1] + distance) / N[2]
        v = np.array([1, 1, z])
        v = v - light_position

        # Normalize v
        v = normalize(v)

        # Finds perpendicular vector to v
        u = np.cross(v, N)

        # Normalize u
        u = normalize(u)

        # Finds the left up point of the rectangle
        light_radius = light.getRadius()
        left_up_point = light_position + (u * (-0.5 * light_radius)) + (v * (-0.5 * light_radius))

        # Define a rectangle on that plane, centered at the light source and as wide as the
        # defined light radius. Divide the rectangle into a grid of N*N cells, where N is the number of shadow rays
        shadow_rays = self.scene_settings.getShadowRays()
        cell_proportion = 1.0 / shadow_rays
        rectangle_height = v * light_radius
        rectangle_width = u * light_radius
        cell_height = cell_proportion * rectangle_height
        cell_width = cell_proportion * rectangle_width

        # Aggregate the values of all rays that were cast and count how many of them hit
        # the required point on the surface.
        num_of_rays = 0
        for i in range(shadow_rays):
            for j in range(shadow_rays):
                # Random points selection to avoid banding
                x = random.random()
                y = random.random()

                # Calculate distance between points
                point_on_cell = left_up_point + (cell_height * (i + x)) + (cell_width * (j + y))
                point_on_surface = ray.getIntersectionPoint()
                p = point_on_cell - point_on_surface
                distance = np.linalg.norm(p)

                # Ray direction
                ray_direction = p / distance

                # Calculate ray base (0.0002 prevents black spots)
                p = point_on_surface + self.black_spots_factor * ray_direction

                # Create ray if intersect with surface to know if no light arrives
                transparency_factor = findTransparencyFactor(p, ray_direction, distance, self.surfaces, self.materials)

                num_of_rays += (1.0 * transparency_factor)

        percentage = num_of_rays / np.power(shadow_rays, 2)
        return percentage

    def calculateTransparencyColor(self, ray, max_recursion):
        # Direction of ray
        ray_direction = ray.getDirection()

        # Point where ray starts (0.0002 prevents black spots)
        p = ray.getIntersectionPoint() + self.black_spots_factor * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.surfaces)

        # Have intersection with surface? continue recursively
        if t != np.inf:
            material_index = surface.getMaterial() - 1
            transparency_ray = Ray(p, ray_direction, p + t * ray_direction, material_index)
            color = self.calculateColor(transparency_ray, self.materials[material_index], surface, max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = np.clip(color, 0, 1)
        return color

    def calculateReflectanceColor(self, ray, N, max_recursion, material):
        # Direction of reflected ray
        R = calculateReflectionDirection(ray.getDirection(), N)

        # Point where ray starts (0.0002 prevents black spots)
        p = ray.getIntersectionPoint() + self.black_spots_factor * R

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, R, self.surfaces)

        # Have intersection with surface? continue recursively
        if t != np.inf:
            material_index = surface.getMaterial() - 1
            reflectance_ray = Ray(p, R, p + t * R, material_index)
            color = self.calculateColor(reflectance_ray, self.materials[material_index], surface, max_recursion - 1)

        color = color * material.getReflectionColor()

        # Prevent overflow which can happen because of the recursion
        color = np.clip(color, 0, 1)
        return color

    # Calculate specular color
    def calculateSpecularColor(self, light, material, N, L, ray_direction):
        # Calculate reflected ray
        R = (N * (2 * N.dot(L))) - L

        # Calculate specular part
        specular = np.dot(R, -ray_direction)
        specular = np.power(specular, material.getShininess())
        specular = specular * material.getSpecularColor() * light.getSpecularIntensity() * light.getColor()
        return specular

    # Calculate color as using phong method
    def calculateSpecularAndDiffuseColor(self, ray, N, material, surface):
        color = np.zeros(3)
        intersection = ray.getIntersectionPoint()
        ray_direction = ray.getDirection()
        for light in self.lights:
            L = light.getPosition() - intersection
            L = normalize(L)

            # Calculate diffuse color part
            dot = L.dot(N)
            if dot < 0:
                continue
            diffuse_and_specular_color = light.getColor() * dot * material.getDiffuseColor()

            # Calculate specular part
            diffuse_and_specular_color += self.calculateSpecularColor(light, material, N, L, ray_direction)

            # Calculate diffuse and specular color
            percentage_of_rays = self.calculateRaysPrecentage(ray, light, -L, surface)
            color += diffuse_and_specular_color * (
                    (1 - light.getShadowIntensity()) + (percentage_of_rays * light.getShadowIntensity()))

        return color

    # Calculate pixel color as instructed in project document
    def calculateColor(self, ray, material, surface, max_recursion):
        # Passed the limit of recursion?
        if max_recursion == 0:
            return self.background_color

        # Init color
        color = np.zeros(3)

        # Get normal
        N = surface.getNormal(ray)

        # Needs the opposite direction of normal?
        ray_direction = ray.getDirection()
        if N.dot(ray_direction) > 0:
            N = -N
        N = normalize(N)

        # Calculate color caused by specular and diffuse
        color += self.calculateSpecularAndDiffuseColor(ray, N, material, surface)

        # Calculate color caused by transparency
        transparency_color = np.zeros(3)
        if material.getTransparency() > 0:
            transparency_color = self.calculateTransparencyColor(ray, max_recursion)

        # Calculate color caused by reflectance
        reflectance_color = np.zeros(3)
        if np.any(material.getReflectionColor() != 0):
            reflectance_color = self.calculateReflectanceColor(ray, N, max_recursion, material)

        # Calculate color of surface
        color = (
                        1 - material.getTransparency()) * color + material.getTransparency() * transparency_color + reflectance_color

        # Prevent overflow which can happen because of the recursion
        color = np.clip(color, 0, 1)
        return color
