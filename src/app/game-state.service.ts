import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

/**
 * Represents the state of a Battleship board.
 * Each cell can be one of:
 * - 'empty': no ship, not shot
 * - 'ship': a ship occupies the cell (only visible on the player's board)
 * - 'hit': a shot hit a ship
 * - 'miss': a shot missed
 */
export type CellState = 'empty' | 'ship' | 'hit' | 'miss';
export type Board = CellState[][];

@Injectable({ providedIn: 'root' })
export class GameStateService {
  private readonly boardSize = 10;

  private playerBoardSubject: BehaviorSubject<Board> = new BehaviorSubject<Board>(this.createEmptyBoard());
  private opponentBoardSubject: BehaviorSubject<Board> = new BehaviorSubject<Board>(this.createEmptyBoard());

  /** Observable streams for components to subscribe to */
  playerBoard$: Observable<Board> = this.playerBoardSubject.asObservable();
  opponentBoard$: Observable<Board> = this.opponentBoardSubject.asObservable();

  /** Create a fresh empty board */
  private createEmptyBoard(): Board {
    return Array.from({ length: this.boardSize }, () =>
      Array.from({ length: this.boardSize }, () => 'empty' as CellState)
    );
  }

  /** Deep clone a board to avoid mutating the original reference */
  private cloneBoard(board: Board): Board {
    return board.map(row => [...row]);
  }

  /** Place a ship on the player's board.
   * @param startX zero‑based column index
   * @param startY zero‑based row index
   * @param size length of the ship
   * @param horizontal true if ship is placed horizontally, false for vertical
   */
  placeShip(startX: number, startY: number, size: number, horizontal: boolean): void {
    const board = this.cloneBoard(this.playerBoardSubject.value);
    for (let i = 0; i < size; i++) {
      const x = horizontal ? startX + i : startX;
      const y = horizontal ? startY : startY + i;
      if (x >= this.boardSize || y >= this.boardSize) {
        // Out of bounds – ignore placement for safety
        continue;
      }
      board[y][x] = 'ship';
    }
    this.playerBoardSubject.next(board);
  }

  /** Record a shot on either board.
   * @param x column index
   * @param y row index
   * @param hit true if the shot hit a ship
   * @param isOpponent true if the shot is on the opponent's board, false for player's own board
   */
  recordShot(x: number, y: number, hit: boolean, isOpponent: boolean): void {
    const subject = isOpponent ? this.opponentBoardSubject : this.playerBoardSubject;
    const board = this.cloneBoard(subject.value);
    board[y][x] = hit ? 'hit' : 'miss';
    subject.next(board);
  }
}
