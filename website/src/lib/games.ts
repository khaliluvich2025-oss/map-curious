/** Where on Earth? rounds: each answer is a discovery's verified coordinate. */
export interface Round { slug: string; clue: string; hint: string }

export const WHERE_ROUNDS: Round[] = [
  { slug: 'centralia-pennsylvania', clue: 'A small town in the eastern United States where a coal-mine fire has burned underground since 1962.', hint: 'Coal country, about 100 miles northwest of Philadelphia.' },
  { slug: 'surtsey-iceland', clue: 'A volcanic island in the North Atlantic that first broke the sea surface in November 1963.', hint: 'Off the south coast of a famously volcanic island nation.' },
  { slug: 'point-roberts-washington', clue: 'A U.S. town on a peninsula that you can only reach by land by driving through another country.', hint: 'Just south of the 49th parallel, near Vancouver.' },
  { slug: 'okavango-delta-botswana', clue: 'A river from the Angolan highlands spreads into a vast inland delta and never reaches the ocean.', hint: 'Southern Africa, on the edge of the Kalahari.' },
  { slug: 'crater-lake-oregon', clue: 'The deepest lake in the United States, filling the bowl of a collapsed volcano.', hint: 'The Cascade Range, south of Portland.' },
  { slug: 'suez-canal-egypt', clue: 'A canal opened in 1869 that links two seas without a single lock.', hint: 'Between the Mediterranean and the Red Sea.' },
  { slug: 'the-gambia', clue: 'Mainland Africa’s smallest country: a thin strip that follows a river inland from the Atlantic.', hint: 'West Africa, surrounded by Senegal.' },
  { slug: 'fort-jefferson-florida', clue: 'An unfinished brick fortress on a tiny island about 70 miles west of the end of a famous ocean highway.', hint: 'Past Key West, in the Gulf.' },
  { slug: 'catatumbo-lightning-venezuela', clue: 'The place with the most lightning on Earth, where a river meets a huge lake.', hint: 'Northwestern South America.' },
  { slug: 'alcatraz-island', clue: 'A rocky island prison, surrounded by cold water and strong currents, that closed in 1963.', hint: 'In a famous Californian bay.' },
];

/** Points for a guess: 1000 at the exact spot, falling off with distance. */
export const scoreFor = (miles: number) => Math.max(0, Math.round(1000 * Math.exp(-miles / 900)));
