import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface ShipPlacement {
  size: number;
  orientation: 'horizontal' | 'vertical';
  startX: number; // 0-indexed column
  startY: number; // 0-indexed row
}

@Component({
  selector: 'app-ship-placement',
  templateUrl: './ship-placement.component.html',
  styleUrls: ['./ship-placement.component.scss']
})
export class ShipPlacementComponent implements OnInit {
  readonly boardSize = 6;
  // Represent board as 2D array for template iteration
  board: number[][] = [];

  // Ships that need to be placed (sizes 2,3,4)
  shipsToPlace: { size: number; placed: boolean; orientation: 'horizontal' | 'vertical' }[] = [
    { size: 2, placed: false, orientation: 'horizontal' },
    { size: 3, placed: false, orientation: 'horizontal' },
    { size: 4, placed: false, orientation: 'horizontal' }
  ];

  // Successful placements
  placements: ShipPlacement[] = [];

  /** Check if a cell is occupied by any placed ship */
  isCellOccupied(x: number, y: number): boolean {
    for (const p of this.placements) {
      const cells = this.getOccupiedCells(p);
      if (cells.some(c => c[0] === x && c[1] === y)) {
        return true;
      }
    }
    return false;
  }

  // Index of currently selected ship (or -1 if none)
  selectedShipIndex: number = -1;

  // Game ID – in a real app this would come from route params
  gameId: string = 'demo-game';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.initBoard();
  }

  private initBoard(): void {
    this.board = Array.from({ length: this.boardSize }, () => Array(this.boardSize).fill(0));
  }

  /** Select a ship to place */
  selectShip(index: number): void {
    if (this.shipsToPlace[index].placed) {
      return; // cannot re‑select already placed ship
    }
    this.selectedShipIndex = index;
  }

  /** Toggle orientation of the currently selected ship */
  toggleOrientation(): void {
    if (this.selectedShipIndex === -1) return;
    const ship = this.shipsToPlace[this.selectedShipIndex];
    ship.orientation = ship.orientation === 'horizontal' ? 'vertical' : 'horizontal';
  }

  /** Handle click on a board cell */
  onCellClick(x: number, y: number): void {
    if (this.selectedShipIndex === -1) return;
    const shipInfo = this.shipsToPlace[this.selectedShipIndex];
    const placement: ShipPlacement = {
      size: shipInfo.size,
      orientation: shipInfo.orientation,
      startX: x,
      startY: y
    };
    if (this.isPlacementValid(placement)) {
      this.placements.push(placement);
      this.shipsToPlace[this.selectedShipIndex].placed = true;
      this.selectedShipIndex = -1;
    } else {
      // In a real UI we would show an error message; for now just console.warn
      console.warn('Invalid ship placement');
    }
  }

  /** Validate placement – bounds and overlap */
  isPlacementValid(p: ShipPlacement): boolean {
    const { startX, startY, size, orientation } = p;
    // Bounds check
    if (orientation === 'horizontal') {
      if (startX + size > this.boardSize) return false;
    } else {
      if (startY + size > this.boardSize) return false;
    }
    // Overlap check
    for (const existing of this.placements) {
      const cellsA = this.getOccupiedCells(p);
      const cellsB = this.getOccupiedCells(existing);
      for (const a of cellsA) {
        for (const b of cellsB) {
          if (a[0] === b[0] && a[1] === b[1]) {
            return false;
          }
        }
      }
    }
    return true;
  }

  /** Return list of [x, y] coordinates occupied by a placement */
  private getOccupiedCells(p: ShipPlacement): [number, number][] {
    const cells: [number, number][] = [];
    for (let i = 0; i < p.size; i++) {
      const x = p.orientation === 'horizontal' ? p.startX + i : p.startX;
      const y = p.orientation === 'vertical' ? p.startY + i : p.startY;
      cells.push([x, y]);
    }
    return cells;
  }

  /** Submit all placements to backend */
  submitPlacements(): Observable<any> {
    const payload = this.placements.map(p => ({
      size: p.size,
      orientation: p.orientation,
      start_x: p.startX,
      start_y: p.startY
    }));
    return this.http.post(`/games/${this.gameId}/ships`, payload);
  }
}
