export type CategoryId =
  | 'geography-mysteries'
  | 'strange-borders'
  | 'abandoned-places'
  | 'hidden-history'
  | 'crime-mysteries'
  | 'natural-wonders';

export interface Category {
  id: CategoryId;
  name: string;
  blurb: string;
  image: string;
}

export const CATEGORIES: Category[] = [
  { id: 'geography-mysteries', name: 'Geography Mysteries', blurb: 'Places that seem impossible', image: '/img/denmark-strait-map.jpg' },
  { id: 'strange-borders', name: 'Strange Borders', blurb: "The world's weirdest boundaries", image: '/img/point-roberts.jpg' },
  { id: 'abandoned-places', name: 'Abandoned Places', blurb: 'Ghost towns and forgotten locations', image: '/img/centralia-map.jpg' },
  { id: 'hidden-history', name: 'Hidden History', blurb: 'Stories buried by time', image: '/img/fort-jefferson-map.jpg' },
  { id: 'crime-mysteries', name: 'Crime & Mysteries', blurb: 'Cases written into the map', image: '/img/db-cooper.jpg' },
  { id: 'natural-wonders', name: 'Natural Wonders', blurb: 'Forces that shape the planet', image: '/img/surtsey.jpg' },
];

export const categoryById = (id: CategoryId) => CATEGORIES.find((c) => c.id === id)!;
