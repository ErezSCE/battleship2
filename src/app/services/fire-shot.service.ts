import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * Service responsible for firing a shot in a Battleship game.
 * It abstracts the HTTP call to the backend endpoint POST /games/{gameId}/shots.
 */
@Injectable({
  providedIn: 'root'
})
export class FireShotService {
  constructor(private http: HttpClient) {}

  /**
   * Fires a shot at the given coordinates for the specified game.
   * @param gameId The identifier of the game.
   * @param x The x coordinate (0-indexed).
   * @param y The y coordinate (0-indexed).
   * @returns Observable emitting the server response.
   */
  fireShot(gameId: string, x: number, y: number): Observable<any> {
    const url = `/games/${gameId}/shots`;
    return this.http.post<any>(url, { x, y });
  }
}
