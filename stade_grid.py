from mesa.space import SingleGrid

class StadeGrid(SingleGrid):
    """A Grid where each cell contains exactly at most one object, and which is toroidal on the x axis."""
    
    def y_out_of_bound(self, pos) -> bool:
        """Determines whether the y coordinate is off the grid"""
        x, y = pos
        return y < 0 or y >= self.height
    
    def x_out_of_bound(self, pos) -> bool:
        """Determines whether the x coordinate is off the grid"""
        x, y = pos
        return x < 0 or x >= self.width
    

    def torus_adj(self, pos):
        """Convert coordinate, handling torus looping."""
        x_out, y_out = self.x_out_of_bound(pos), self.y_out_of_bound(pos)
        if not x_out and not y_out:
            return pos
        elif y_out or not self.torus:
            raise Exception("Point out of bounds, and space non-toroidal.")
        else:
            return pos[0] % self.width, pos[1]

    def get_neighborhood(
        self,
        pos,
        moore,
        include_center = False,
        radius= 1,
    ) :
        """Return a list of cells that are in the neighborhood of a
        certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                   (including diagonals)
                   If False, return Von Neumann neighborhood
                   (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of coordinate tuples representing the neighborhood;
            With radius 1, at most 9 if Moore, 5 if Von Neumann (8 and 4
            if not including the center).
        """
        cache_key = (pos, moore, include_center, radius)
        neighborhood = self._neighborhood_cache.get(cache_key, None)

        if neighborhood is None:
            coordinates = set()

            x, y = pos
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx == 0 and dy == 0 and not include_center:
                        continue
                    # Skip coordinates that are outside manhattan distance
                    if not moore and abs(dx) + abs(dy) > radius:
                        continue

                    coord = (x + dx, y + dy)

                    if self.out_of_bounds(coord):
                        # Skip if not a torus and new coords out of bounds.
                        if not self.torus or self.y_out_of_bound(coord):
                            continue
                        coord = self.torus_adj(coord)

                    coordinates.add(coord)

            neighborhood = sorted(coordinates)
            self._neighborhood_cache[cache_key] = neighborhood

        return neighborhood