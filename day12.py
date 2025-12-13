import sys

class Solve:
    def __init__(self, filename):
        self.shapes = {}    
        self.regions = []
        self.mask_cache = {} 
        self.parse_input(filename)

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]


        curr_id, curr_grid = None, []
        
        for line in lines:
            if not line:
                if curr_id is not None:
                    self.save_shape(curr_id, curr_grid)
                    curr_id, curr_grid = None, []
                continue
            
            if ':' in line and 'x' in line.split(':')[0]:
                parts = line.split(':')
                dims = parts[0].split('x')
                self.regions.append({
                    'w': int(dims[0]), 
                    'h': int(dims[1]), 
                    'reqs': list(map(int, parts[1].split()))
                })
            elif ':' in line:
                if curr_id is not None:
                    self.save_shape(curr_id, curr_grid)
                curr_id = int(line.split(':')[0])
                curr_grid = []
            else:
                curr_grid.append(line)
        
        if curr_id is not None:
            self.save_shape(curr_id, curr_grid)

    def save_shape(self, id, grid):
        coords = set()
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char == '#': coords.add((r, c))
        self.shapes[id] = coords

    def get_orientations(self, id):
        base = self.shapes[id]
        vars = set()
        
        def normalize(coords):
            mr = min(r for r,c in coords)
            mc = min(c for r,c in coords)
            return tuple(sorted((r-mr, c-mc) for r,c in coords))

        curr = base
        for _ in range(2): 
            for _ in range(4): 
                vars.add(normalize(curr))
                curr = {(c, -r) for r,c in curr}
            curr = {(-r, c) for r,c in base}
        return list(vars)

    def precompute_masks(self, shape_id, W, H):
        cache_key = (shape_id, W, H)
        if cache_key in self.mask_cache:
            return self.mask_cache[cache_key]

        masks = []
        orientations = self.get_orientations(shape_id)
        
        for shape in orientations:
            h_s = max(r for r,c in shape) + 1
            w_s = max(c for r,c in shape) + 1
            
            if h_s > H or w_s > W: continue
            
            for r in range(H - h_s + 1):
                for c in range(W - w_s + 1):
                    m = 0
                    for pr, pc in shape:
                        m |= (1 << ((r + pr) * W + (c + pc)))
                    masks.append(m)
        
        self.mask_cache[cache_key] = masks
        return masks

    def solve(self):
        count = 0
        for i, reg in enumerate(self.regions):
            if self.solve_single_region(reg):
                count += 1
        
        print(count)

    def solve_single_region(self, reg):
        W, H = reg['w'], reg['h']
        
        pieces = []
        for pid, qty in enumerate(reg['reqs']):
            if qty == 0: continue
            
            masks = self.precompute_masks(pid, W, H)
            if not masks: return False 
            
            for _ in range(qty):
                pieces.append({'id': pid, 'masks': masks})
        
        pieces.sort(key=lambda p: len(p['masks']))
        
        total_area = sum(len(self.shapes[p['id']]) for p in pieces)
        if total_area > W * H: return False

        n = len(pieces)
        prev_same = [-1] * n
        for i in range(1, n):
            if pieces[i]['id'] == pieces[i-1]['id']:
                prev_same[i] = i - 1

        indices = [-1] * n 

        def backtrack(k, board):
            if k == n: 
                return True
            
            masks = pieces[k]['masks']
            
            start_id = 0
            if prev_same[k] != -1:
                start_id = indices[prev_same[k]] + 1
            
            for i in range(start_id, len(masks)):
                m = masks[i]
                if not (board & m):
                    indices[k] = i
                    if backtrack(k + 1, board | m):
                        return True
            return False

        return backtrack(0, 0)

if __name__ == '__main__':
    Solve('day12_input.txt').solve()