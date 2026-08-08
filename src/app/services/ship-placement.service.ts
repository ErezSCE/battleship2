import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ShipPlacementService {
  constructor(private http: HttpClient) {}

  /**
   * Sends ship placement data to the backend for a specific game.
   * @param gameId The identifier of the game.
   * @param payload The array of ship placement objects.
   * @returns Observable of the HTTP response.
   */
  placeShips(gameId: string, payload: any): Observable<any> {
    return this.http.post(`/games/${gameId}/ships`, payload);
  }
}
