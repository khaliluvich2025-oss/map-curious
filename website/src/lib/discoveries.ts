import type { CategoryId } from './categories';

export interface Source { label: string; url: string }
export interface Discovery {
  slug: string;
  name: string;
  place: string;
  country: string;
  lat: number;
  lng: number;
  coordNote?: string;          // shown when the pin marks an area rather than an exact point
  category: CategoryId;
  featured?: boolean;
  image: string;
  summary: string;             // one line for cards
  intro: string;               // hook paragraph
  story: string[];             // fact-checked body
  facts: string[];             // quick facts
  sources: Source[];
  unresolved?: boolean;        // open case: never present a solution
}

const NPS = (park: string, path = ''): Source => ({ label: `National Park Service · ${park}`, url: `https://www.nps.gov/${path}` });

export const DISCOVERIES: Discovery[] = [
  {
    slug: 'denmark-strait-cataract', name: 'The Underwater Waterfall', place: 'Denmark Strait', country: 'Between Greenland and Iceland',
    lat: 66.0, lng: -27.0, coordNote: 'Approximate location of the strait’s undersea ridge.', category: 'geography-mysteries', featured: true,
    image: '/img/denmark-strait.jpg',
    summary: 'Earth’s largest known waterfall is hidden beneath the North Atlantic.',
    intro: 'From above, the Denmark Strait looks like ordinary ocean. Beneath the surface, cold water pours over an undersea ridge and drops more than two miles.',
    story: [
      'North of the strait, in the Nordic Seas, the water is extremely cold, and cold water is denser than warm water. When it flows south and meets the warmer, lighter water of the Atlantic, it does not mix. It sinks beneath it.',
      'At the edge of an undersea ridge, that heavy water spills down the slope toward the deep ocean floor. NOAA puts the drop at roughly 11,500 feet (about 3,500 m), more than three times the height of Angel Falls, the tallest waterfall on land.',
      'It is water falling through water, invisible from the surface. But its flow is enormous, and the cold, sinking water helps drive the ocean currents that move heat around the planet.',
    ],
    facts: ['Drop: ≈11,500 ft (3,500 m)', 'Estimated flow: more than 123 million cubic feet per second (NOAA)', 'Detected only with scientific instruments'],
    sources: [{ label: 'NOAA Ocean Service · Earth’s largest waterfall', url: 'https://oceanservice.noaa.gov/facts/largest-waterfall.html' }],
  },
  {
    slug: 'surtsey-iceland', name: 'The Island Born in 1963', place: 'Surtsey, Westman Islands', country: 'Iceland',
    lat: 63.303, lng: -20.605, category: 'natural-wonders', featured: true, image: '/img/surtsey.jpg',
    summary: 'A volcanic island that rose from the sea in 1963, and is slowly being taken back.',
    intro: 'In November 1963, fishermen off Iceland’s south coast spotted dark smoke rising from the sea. It wasn’t a ship on fire. An underwater volcano was erupting.',
    story: [
      'Within a day, a brand-new island broke the surface. Iceland named it Surtsey, after a fire giant from Norse mythology. The eruptions continued until June 1967, when the island covered about one square mile.',
      'Scientists then decided to leave it almost untouched. Only researchers may land, and they take care not to bring seeds or insects. Surtsey became a natural laboratory for watching life arrive on bare rock: seeds carried by sea and wind, insects, birds, then plants.',
      'Surtsey was added to the UNESCO World Heritage List in 2008. But the sea is winning: waves have worn away roughly half of its original area.',
    ],
    facts: ['Eruption: 1963–1967', 'Peak area: ≈2.65 km² (≈1 sq mi)', 'UNESCO World Heritage Site since 2008'],
    sources: [{ label: 'UNESCO World Heritage Centre · Surtsey', url: 'https://whc.unesco.org/en/list/1267' }],
  },
  {
    slug: 'centralia-pennsylvania', name: 'The Town That Has Been Burning Since 1962', place: 'Centralia, Pennsylvania', country: 'United States',
    lat: 40.8043, lng: -76.3402, category: 'abandoned-places', featured: true, image: '/img/centralia.jpg',
    summary: 'A coal-mine fire has burned beneath this Pennsylvania town for more than sixty years.',
    intro: 'Centralia sits on top of a coal seam. In 1962 a fire started in the area, possibly while a dump was being burned, and it crept into the old mines beneath the town.',
    story: [
      'Underground, the fire found an endless supply of fuel. Smoke and dangerous gases rose through cracks in yards and roads. In 1981, 12-year-old Todd Domboski fell into a steaming sinkhole that opened beneath him; he survived.',
      'In the 1980s the federal government funded a buyout, and nearly all residents moved away. Most houses were torn down, and in 2002 the U.S. Postal Service discontinued the town’s ZIP code.',
      'The fire is still burning, moving slowly through the coal. Some estimates say it could last for centuries.',
    ],
    facts: ['Fire began: 1962', 'Federal relocation funding: ≈$42 million (1980s)', 'ZIP code 17927 discontinued in 2002'],
    sources: [{ label: 'Environment & Society Portal · Centralia Mine Fire', url: 'https://www.environmentandsociety.org/node/6551' }],
  },
  {
    slug: 'fort-jefferson-florida', name: 'The Fortress at the End of the Road', place: 'Dry Tortugas, Florida', country: 'United States',
    lat: 24.6285, lng: -82.8732, category: 'hidden-history', featured: true, image: '/img/fort-jefferson.jpg',
    summary: 'A massive brick fort, about 70 miles west of Key West, that was never finished.',
    intro: 'About seventy miles west of Key West, past the end of the road, a tiny cluster of islands holds a massive brick fortress.',
    story: [
      'Fort Jefferson was started in 1846 to guard the shipping lanes between the Gulf of Mexico and the Atlantic. Work went on for about thirty years, but the fort was never finished: rifled cannon could smash brick walls, and the heavy structure was settling and cracking on its sand-and-coral foundation.',
      'During and after the Civil War the fort served as a prison. Its best-known inmate was Dr. Samuel Mudd, convicted after setting the broken leg of John Wilkes Booth. He was pardoned in 1869.',
      'Today it is the heart of Dry Tortugas National Park, reachable only by boat or seaplane.',
    ],
    facts: ['Construction began: 1846', 'Never completed', 'Access: boat or seaplane only'],
    sources: [NPS('Dry Tortugas National Park', 'drto/')],
  },
  {
    slug: 'db-cooper-mystery', name: 'The Hijacker Who Vanished', place: 'Southwest Washington', country: 'United States',
    lat: 45.716, lng: -122.775, coordNote: 'Pin marks Tena Bar on the Columbia River, where ransom money was found in 1980. The jump site is unknown.',
    category: 'crime-mysteries', featured: true, unresolved: true, image: '/img/db-cooper.jpg',
    summary: 'In 1971 a man jumped from a jet with $200,000 and was never found.',
    intro: 'On November 24, 1971, a man who bought his ticket as “Dan Cooper” boarded a Northwest Orient flight from Portland to Seattle, and handed a flight attendant a note: he had a bomb.',
    story: [
      'In Seattle he traded the passengers for $200,000 and four parachutes, then ordered the crew to fly south, low and slow. Somewhere over southwest Washington, at night and in the rain, he lowered the rear stairs and jumped.',
      'In 1980 a boy digging along the Columbia River found about $5,800 of the ransom money; the serial numbers matched. No body and no parachute have been confirmed.',
      'In 2016 the FBI stopped actively investigating. The case remains unsolved; whether he survived the jump is an open question.',
    ],
    facts: ['Date: Nov 24, 1971', 'Ransom: $200,000', 'Status: unsolved (FBI ended active investigation in 2016)'],
    sources: [{ label: 'FBI · D.B. Cooper Hijacking', url: 'https://www.fbi.gov/history/famous-cases/db-cooper-hijacking' }],
  },
  {
    slug: 'hudson-river-new-york', name: 'The River That Flows Both Ways', place: 'Hudson River, New York', country: 'United States',
    lat: 42.7522, lng: -73.6864, coordNote: 'Pin marks the Federal Dam at Troy, the head of the tide.', category: 'geography-mysteries',
    image: '/img/hudson.jpg',
    summary: 'Twice a day the lower Hudson’s current turns around and flows north.',
    intro: 'The Hudson begins in New York’s Adirondack Mountains and runs south to New York City. But its lower half is not really a river: it is an estuary, an arm of the sea.',
    story: [
      'Twice a day, ocean tides push in from New York Harbor and reverse the current. The tide reaches about 150 miles upstream, to the Federal Dam at Troy, near Albany.',
      'In dry summers, when less fresh water comes down from the mountains, salty ocean water can push about 60 miles up the river.',
      'One Native name for the Hudson is often translated as “the river that flows both ways.”',
    ],
    facts: ['Tidal reach: ≈150 miles, to Troy', 'Salt front: up to ≈60 miles upriver in droughts', 'Tides: twice a day'],
    sources: [{ label: 'NYS DEC · Hudson River Estuary', url: 'https://dec.ny.gov/nature/waterbodies/rivers/hudson-river-estuary' }],
  },
  {
    slug: 'mount-st-helens-washington', name: 'The Mountain That Lost 1,300 Feet', place: 'Mount St. Helens, Washington', country: 'United States',
    lat: 46.1912, lng: -122.1944, category: 'natural-wonders', image: '/img/mount-st-helens.jpg',
    summary: 'On May 18, 1980, an eruption removed about 1,300 feet from the summit.',
    intro: 'On May 18, 1980, an earthquake shook loose the north side of Mount St. Helens, triggering the largest landslide in recorded history.',
    story: [
      'With that weight suddenly gone, pressure inside blasted sideways, flattening forests across about 230 square miles. Fifty-seven people died.',
      'An ash column climbed about 15 miles high, and ash eventually fell in 11 states.',
      'The cause lies offshore: the Pacific Northwest sits above a subduction zone that feeds the volcanoes of the Cascade Range.',
    ],
    facts: ['Date: May 18, 1980', 'Summit lost: ≈1,300 ft', 'Ash fell in 11 states'],
    sources: [{ label: 'USGS · Mount St. Helens', url: 'https://www.usgs.gov/volcanoes/mount-st-helens' }],
  },
  {
    slug: 'niagara-falls', name: 'The Waterfall That Is Moving', place: 'Niagara Falls', country: 'United States / Canada',
    lat: 43.0799, lng: -79.0747, category: 'natural-wonders', image: '/img/niagara-falls.jpg',
    summary: 'Over about 12,000 years, the falls have worn roughly 7 miles upstream.',
    intro: 'In 1969, engineers shut off the American Falls to study a slow problem: the falls are moving.',
    story: [
      'About 12,000 years ago the falls began at the Niagara Escarpment. Since then they have worn their way roughly seven miles upstream, carving the Niagara Gorge.',
      'A hard cap layer sits on softer shale. Falling water scours the soft rock until the ledge above breaks off.',
      'Erosion is much slower today, partly because water is diverted for hydropower.',
    ],
    facts: ['Retreat: ≈7 miles in ≈12,000 years', 'American Falls dewatered: 1969'],
    sources: [{ label: 'Niagara Parks / NYS Parks · Niagara Falls geology', url: 'https://www.niagarafallsstatepark.com/' }],
  },
  {
    slug: 'thingvellir-iceland-rift', name: 'The Island Being Pulled Apart', place: 'Þingvellir National Park', country: 'Iceland',
    lat: 64.2559, lng: -21.1299, category: 'geography-mysteries', image: '/img/iceland-rift.jpg',
    summary: 'Iceland sits on the Mid-Atlantic Ridge, where two plates move apart.',
    intro: 'Iceland sits right on top of the Mid-Atlantic Ridge, the seam between the North American and Eurasian plates.',
    story: [
      'The plates move apart by about two centimeters a year, roughly as fast as fingernails grow. Most of the ridge lies deep underwater, but in Iceland it rises above the sea.',
      'At Þingvellir National Park you can walk through a rift valley between the two plates. Rising magma fills the gap, which is why Iceland has so many volcanoes.',
    ],
    facts: ['Spreading rate: ≈2 cm per year', 'Rift valley visible at Þingvellir'],
    sources: [{ label: 'USGS · Understanding plate motions', url: 'https://pubs.usgs.gov/gip/dynamic/understanding.html' }],
  },
  {
    slug: 'overseas-highway-florida', name: 'The Highway Across the Ocean', place: 'Florida Keys', country: 'United States',
    lat: 24.705, lng: -81.15, coordNote: 'Pin marks the Seven Mile Bridge.', category: 'hidden-history', image: '/img/overseas-highway.jpg',
    summary: 'More than 100 miles of road linking mainland Florida to Key West over about 40 bridges.',
    intro: 'The Overseas Highway links mainland Florida to Key West through a chain of islands, crossing about forty bridges, including the Seven Mile Bridge.',
    story: [
      'The route began as Henry Flagler’s Overseas Railroad, which reached Key West in 1912. The 1935 Labor Day hurricane wrecked long sections of it.',
      'Instead of rebuilding the railroad, the route was turned into a road, which opened in 1938. At the end of it, Key West sits about 90 miles from Cuba.',
    ],
    facts: ['Railroad reached Key West: 1912', 'Highway opened: 1938', 'Key West to Cuba: ≈90 miles'],
    sources: [{ label: 'Florida Department of Transportation', url: 'https://www.fdot.gov/' }],
  },
  {
    slug: 'chicxulub-crater-mexico', name: 'The Dinosaur-Killer Crater', place: 'Yucatán Peninsula', country: 'Mexico',
    lat: 21.4, lng: -89.5, coordNote: 'Approximate center of the buried crater.', category: 'geography-mysteries', image: '/img/chicxulub-crater.jpg',
    summary: 'The asteroid impact that ended the age of dinosaurs left a buried crater about 110 miles wide.',
    intro: 'About 66 million years ago, a rock roughly six miles wide slammed into a shallow sea at the northern tip of the Yucatán Peninsula.',
    story: [
      'It blasted a crater about 110 miles across and helped wipe out around three-quarters of all species on Earth, including the non-avian dinosaurs.',
      'Today the crater is buried under limestone, half on land and half under the Gulf of Mexico. Its edge is traced by a curving ring of sinkholes called cenotes.',
    ],
    facts: ['Age: ≈66 million years', 'Diameter: ≈110 miles (≈180 km)'],
    sources: [{ label: 'NASA · Chicxulub impact', url: 'https://science.nasa.gov/' }],
  },
  {
    slug: 'crater-lake-oregon', name: 'The Deepest Lake in America', place: 'Crater Lake, Oregon', country: 'United States',
    lat: 42.9446, lng: -122.109, category: 'natural-wonders', image: '/img/crater-lake.jpg',
    summary: 'A 1,943-foot-deep lake inside a collapsed volcano.',
    intro: 'About 7,700 years ago, Mount Mazama erupted so violently that its summit collapsed, leaving a bowl called a caldera.',
    story: [
      'Over centuries, rain and snow filled the caldera. No rivers flow in and none flow out.',
      'At 1,943 feet, Crater Lake is the deepest lake in the United States, and because its water falls almost entirely from the sky, it is among the clearest on Earth.',
    ],
    facts: ['Depth: 1,943 ft', 'Formed: ≈7,700 years ago'],
    sources: [NPS('Crater Lake National Park', 'crla/')],
  },
  {
    slug: 'erie-canal-new-york', name: 'The Ditch That Built New York', place: 'Erie Canal, New York', country: 'United States',
    lat: 43.1706, lng: -78.6903, coordNote: 'Pin marks the locks at Lockport.', category: 'hidden-history', image: '/img/erie-canal.jpg',
    summary: 'An 1825 canal that helped make New York City America’s busiest port.',
    intro: 'Critics called it “Clinton’s Ditch.” When the Erie Canal opened in 1825, it changed the map of American trade.',
    story: [
      'The canal ran about 363 miles across upstate New York, from Albany on the Hudson to Buffalo on Lake Erie. Because the land rises about 570 feet heading west, builders needed 83 locks.',
      'Shipping costs fell by roughly 90 percent, helping make New York City the country’s busiest port.',
    ],
    facts: ['Opened: 1825', 'Length: ≈363 miles', 'Original locks: 83'],
    sources: [{ label: 'New York State Canal Corporation', url: 'https://www.canals.ny.gov/' }],
  },
  {
    slug: 'mount-rainier-washington', name: 'The Volcano Seattle Can See', place: 'Mount Rainier, Washington', country: 'United States',
    lat: 46.8523, lng: -121.7603, category: 'natural-wonders', image: '/img/mount-rainier.jpg',
    summary: 'The most glaciated peak in the lower 48, about 60 miles from Seattle.',
    intro: 'Mount Rainier rises about 14,400 feet, roughly 60 miles southeast of Seattle, and holds more glacier ice than any other peak in the lower 48 states.',
    story: [
      'That ice is the danger. If the volcano heats up, melting snow and ice can mix with loose rock into huge mudflows called lahars.',
      'About 5,600 years ago one of these, the Osceola Mudflow, reached the Puget Sound lowlands where towns like Auburn stand today. Valley communities now have warning sirens and marked evacuation routes.',
    ],
    facts: ['Height: ≈14,410 ft', 'Last eruption: ≈1,000 years ago', 'Main hazard: lahars'],
    sources: [{ label: 'USGS · Mount Rainier', url: 'https://www.usgs.gov/volcanoes/mount-rainier' }],
  },
  {
    slug: 'greenland-ice-sheet', name: 'Greenland’s Hidden Ice Giant', place: 'Greenland Ice Sheet', country: 'Greenland (Denmark)',
    lat: 72.5796, lng: -38.4592, coordNote: 'Pin marks Summit Station, near the top of the ice sheet.', category: 'natural-wonders', image: '/img/greenland-ice.jpg',
    summary: 'Ice nearly two miles thick, heavy enough to push the land below sea level.',
    intro: 'Greenland is hiding a sheet of ice nearly two miles thick, covering about 80 percent of the island.',
    story: [
      'In the middle, the ice is so heavy that it has pushed the land beneath it below sea level. If all of it melted, global sea level would rise about 24 feet.',
      'In recent decades Greenland has been losing hundreds of billions of tons of ice a year.',
    ],
    facts: ['Max thickness: ≈2 miles', 'Sea-level equivalent: ≈24 ft'],
    sources: [{ label: 'NSIDC · Greenland Ice Sheet', url: 'https://nsidc.org/learn/parts-cryosphere/ice-sheets' }],
  },
  {
    slug: 'everglades-river-of-grass', name: 'The River of Grass', place: 'Everglades, Florida', country: 'United States',
    lat: 25.2866, lng: -80.8987, category: 'natural-wonders', image: '/img/everglades.jpg',
    summary: 'Not a swamp but a slow, shallow river up to about 60 miles wide.',
    intro: 'The Everglades is not really a swamp. It is a river: water spills south from Lake Okeechobee in a shallow sheet up to about 60 miles wide.',
    story: [
      'It creeps toward Florida Bay through tall sawgrass. Writer Marjory Stoneman Douglas called it the River of Grass in 1947, the same year Everglades National Park was dedicated.',
      'Canals, farms and cities have drained much of it; today the Everglades is about half its original size, and a major restoration effort aims to send water south again.',
    ],
    facts: ['Sheet flow: up to ≈60 miles wide', 'National Park dedicated: 1947'],
    sources: [NPS('Everglades National Park', 'ever/')],
  },
  {
    slug: 'okavango-delta-botswana', name: 'The River That Never Reaches the Ocean', place: 'Okavango Delta', country: 'Botswana',
    lat: -19.3, lng: 22.9, coordNote: 'Approximate center of the delta.', category: 'natural-wonders', image: '/img/okavango-delta.jpg',
    summary: 'A river that flows into the Kalahari and disappears.',
    intro: 'The Okavango River rises in the highlands of Angola and flows southeast, but it never reaches the sea. It spreads into the Kalahari and vanishes.',
    story: [
      'In Botswana the river fans out into a vast inland delta of channels, lagoons and islands. Almost all of its water is lost to evaporation and plants.',
      'Rain falls in Angola months earlier, so the flood peaks in the dry season, drawing huge numbers of animals. The delta became a UNESCO World Heritage Site in 2014.',
    ],
    facts: ['Type: inland delta (no outlet to the sea)', 'UNESCO World Heritage Site: 2014'],
    sources: [{ label: 'UNESCO World Heritage Centre · Okavango Delta', url: 'https://whc.unesco.org/en/list/1432' }],
  },
  {
    slug: 'suez-canal-egypt', name: 'The Canal With No Locks', place: 'Suez Canal', country: 'Egypt',
    lat: 30.6, lng: 32.33, coordNote: 'Pin marks the canal near Ismailia.', category: 'hidden-history', image: '/img/suez-canal.jpg',
    summary: 'A sea-level canal linking the Mediterranean and the Red Sea since 1869.',
    intro: 'Opened in 1869, the Suez Canal connects the Mediterranean and the Red Sea across about 120 miles of Egyptian desert.',
    story: [
      'Unlike the Panama Canal, it needs no locks: the two seas are at nearly the same level, so ships sail through at sea level.',
    ],
    facts: ['Opened: 1869', 'Length: ≈120 miles (193 km)', 'Locks: none'],
    sources: [{ label: 'Suez Canal Authority', url: 'https://www.suezcanal.gov.eg/' }],
  },
  {
    slug: 'manicouagan-quebec', name: 'The Ring Lake With Two Origins', place: 'Manicouagan Reservoir, Québec', country: 'Canada',
    lat: 51.38, lng: -68.7, category: 'geography-mysteries', image: '/img/manicouagan.jpg',
    summary: 'An ancient impact crater, turned into a ring-shaped lake by a modern dam.',
    intro: 'Seen from space, Manicouagan looks like a giant eye. Its shape comes from an asteroid impact about 214 million years ago.',
    story: [
      'The ring itself is natural: erosion of the ancient impact structure left a circular depression. The water filling it is modern: the Daniel-Johnson Dam, completed in 1968, flooded it into a reservoir.',
    ],
    facts: ['Impact: ≈214 million years ago', 'Ring lake diameter: ≈70 km (≈43 mi)', 'Reservoir: created by a 1960s dam'],
    sources: [{ label: 'NASA Earth Observatory · Manicouagan', url: 'https://earthobservatory.nasa.gov/' }],
  },
  {
    slug: 'chamizal-us-mexico-border', name: 'The River That Moved a Border', place: 'El Paso / Ciudad Juárez', country: 'United States / Mexico',
    lat: 31.766, lng: -106.45, category: 'strange-borders', image: '/img/chamizal-rio-grande.jpg',
    summary: 'When the Rio Grande shifted, a century-long border dispute followed.',
    intro: 'The U.S.–Mexico border follows the Rio Grande. In the 1860s the river shifted south, leaving a tract called El Chamizal on the U.S. side.',
    story: [
      'Both countries claimed the land for about a century. The 1963 Chamizal Convention finally settled it, returning most of the tract to Mexico and moving the river into a new concrete-lined channel.',
    ],
    facts: ['Dispute began: 1860s', 'Settled: 1963 Chamizal Convention'],
    sources: [NPS('Chamizal National Memorial', 'cham/')],
  },
  {
    slug: 'alcatraz-island', name: 'The Prison Built to Be Inescapable', place: 'Alcatraz Island, San Francisco Bay', country: 'United States',
    lat: 37.8267, lng: -122.423, category: 'crime-mysteries', unresolved: true, image: '/img/alcatraz.jpg',
    summary: 'Cold water and strong currents surrounded America’s most famous federal prison.',
    intro: 'From 1934 to 1963, Alcatraz was a federal penitentiary on a rock in San Francisco Bay, surrounded by cold water and strong currents.',
    story: [
      'Over its years as a federal prison, 36 men tried to escape in 14 attempts. Most were caught or died.',
      'In June 1962, Frank Morris and brothers John and Clarence Anglin disappeared from the island. Their fate has never been confirmed, and the case remains open.',
    ],
    facts: ['Federal prison: 1934–1963', 'Escape attempts: 14 (36 men)', 'The 1962 escape remains unresolved'],
    sources: [NPS('Alcatraz Island', 'alca/')],
  },
  {
    slug: 'hawaii-hotspot', name: 'The Plate That Built Hawaii', place: 'Hawaiian Islands', country: 'United States',
    lat: 19.6, lng: -155.5, coordNote: 'Pin marks the Island of Hawaiʻi, the youngest island.', category: 'natural-wonders', image: '/img/hawaii-hotspot.jpg',
    summary: 'The islands line up like a conveyor belt over a volcanic hotspot.',
    intro: 'The Hawaiian Islands sit in the middle of the Pacific Plate, far from any plate boundary. They were built by a hotspot.',
    story: [
      'As the Pacific Plate slides northwest over the hotspot, each volcano is carried away and a new one forms. That is why the islands get older to the northwest, and the Island of Hawaiʻi, home to active Kīlauea, is the youngest.',
    ],
    facts: ['Youngest island: Hawaiʻi (the Big Island)', 'Islands age toward the northwest'],
    sources: [{ label: 'USGS Hawaiian Volcano Observatory', url: 'https://www.usgs.gov/observatories/hvo' }],
  },
  {
    slug: 'point-roberts-washington', name: 'The U.S. Town You Reach Through Canada', place: 'Point Roberts, Washington', country: 'United States',
    lat: 48.985, lng: -123.068, category: 'strange-borders', image: '/img/point-roberts.jpg',
    summary: 'A piece of Washington State cut off by the 49th parallel.',
    intro: 'When the 1846 Oregon Treaty set the U.S.–Canada border along the 49th parallel, it sliced off the tip of a peninsula.',
    story: [
      'That tip, Point Roberts, is part of Washington State, but by land you can reach it only by driving through Canada, crossing the border twice.',
    ],
    facts: ['Border set by: 1846 Oregon Treaty', 'Land access: only through Canada'],
    sources: [{ label: 'U.S. Customs and Border Protection · Point Roberts', url: 'https://www.cbp.gov/' }],
  },
  {
    slug: 'michigan-upper-peninsula', name: 'Why Michigan Has Two Peninsulas', place: 'Upper Peninsula, Michigan', country: 'United States',
    lat: 46.5, lng: -87.0, coordNote: 'Approximate center of the Upper Peninsula.', category: 'strange-borders', image: '/img/michigan-peninsulas.jpg',
    summary: 'A border dispute with Ohio over Toledo shaped Michigan’s map.',
    intro: 'In the 1830s, Michigan and Ohio both claimed a strip of land that included Toledo. The standoff became known as the Toledo War.',
    story: [
      'Congress gave the Toledo Strip to Ohio. In exchange, Michigan received most of the Upper Peninsula, and joined the Union in 1837. Since 1957 the Mackinac Bridge has connected the two halves.',
    ],
    facts: ['Toledo War: 1835–1836', 'Statehood: 1837', 'Mackinac Bridge opened: 1957'],
    sources: [{ label: 'State of Michigan · History', url: 'https://www.michigan.gov/' }],
  },
  {
    slug: 'catatumbo-lightning-venezuela', name: 'The Lake Where Lightning Keeps Striking', place: 'Lake Maracaibo', country: 'Venezuela',
    lat: 9.45, lng: -71.75, coordNote: 'Approximate area where the Catatumbo River meets the lake.', category: 'natural-wonders', image: '/img/catatumbo-lightning.jpg',
    summary: 'Satellite data rank Lake Maracaibo as Earth’s top lightning hotspot.',
    intro: 'Where the Catatumbo River meets Lake Maracaibo, thunderstorms build night after night.',
    story: [
      'Warm lake water, surrounding mountains and colliding winds create storms on a huge share of nights. NASA satellite data identify Lake Maracaibo as the place with the most lightning on Earth.',
    ],
    facts: ['Earth’s lightning hotspot (NASA satellite data)'],
    sources: [{ label: 'NASA · Earth’s lightning hotspots', url: 'https://science.nasa.gov/' }],
  },
  {
    slug: 'the-gambia', name: 'The Country Shaped Like a River', place: 'The Gambia', country: 'The Gambia',
    lat: 13.44, lng: -15.31, coordNote: 'Approximate center of the country.', category: 'strange-borders', image: '/img/the-gambia.jpg',
    summary: 'A thin country that follows the Gambia River, surrounded by Senegal.',
    intro: 'The Gambia is mainland Africa’s smallest country: a long, narrow strip that follows the Gambia River inland from the Atlantic.',
    story: [
      'Apart from its short coastline, it is surrounded by Senegal. Its shape comes from colonial-era agreements between Britain and France that drew the border along the river.',
    ],
    facts: ['Smallest country on mainland Africa', 'Surrounded by Senegal except at the coast'],
    sources: [{ label: 'CIA World Factbook · The Gambia', url: 'https://www.cia.gov/the-world-factbook/countries/gambia-the/' }],
  },
  {
    slug: 'france-brazil-border', name: 'France’s Longest Border Is With Brazil', place: 'Oyapock River', country: 'France (French Guiana) / Brazil',
    lat: 3.84, lng: -51.83, coordNote: 'Pin marks the Oyapock River bridge area.', category: 'strange-borders', image: '/img/france-brazil-border.jpg',
    summary: 'French Guiana makes Brazil France’s longest land neighbor.',
    intro: 'French Guiana, in South America, is not a colony: it is part of France. That gives France a land border with Brazil.',
    story: [
      'At about 730 km (≈450 mi), the border with Brazil is France’s longest land border, longer than any in Europe.',
    ],
    facts: ['Length: ≈730 km', 'French Guiana: an overseas region of France'],
    sources: [{ label: 'CIA World Factbook · French Guiana / France', url: 'https://www.cia.gov/the-world-factbook/countries/france/' }],
  },
  {
    slug: 'angel-island-california', name: 'The Poems on Angel Island’s Walls', place: 'Angel Island, San Francisco Bay', country: 'United States',
    lat: 37.8609, lng: -122.4326, category: 'hidden-history', image: '/img/angel-island.jpg',
    summary: 'Detained immigrants carved poems into the walls of a bay immigration station.',
    intro: 'From 1910 to 1940, the Angel Island Immigration Station processed hundreds of thousands of people arriving on the West Coast.',
    story: [
      'Many detainees, especially from China under the Chinese Exclusion Act, were held for weeks or months. Some carved poems into the wooden walls describing their journey and frustration. Many of those poems survive today.',
    ],
    facts: ['Operated: 1910–1940', 'Now a National Historic Landmark'],
    sources: [{ label: 'Angel Island Immigration Station Foundation', url: 'https://www.aiisf.org/' }],
  },
];

export const discoveryBySlug = (slug: string) => DISCOVERIES.find((d) => d.slug === slug);
export const featuredDiscoveries = DISCOVERIES.filter((d) => d.featured);
export function relatedDiscoveries(d: Discovery, n = 3): Discovery[] {
  const same = DISCOVERIES.filter((x) => x.slug !== d.slug && x.category === d.category);
  const rest = DISCOVERIES.filter((x) => x.slug !== d.slug && x.category !== d.category);
  return [...same, ...rest].slice(0, n);
}
