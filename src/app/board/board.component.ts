import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { Observable } from 'rxjs';
import { GameStateService, Board } from '../game-state.service';

/**
 * BoardComponent displays the player's own board.
 * It shows ship placements, hit markers, and miss markers.
 */
@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit, OnDestroy {

  board$!: Observable<Board>;

  constructor(private gameState: GameStateService) {}

  ngOnInit(): void {
    this.board$ = this.gameState.playerBoard$;
    this.boardSubscription = this.board$.subscribe(board => {
      console.log('BoardComponent: board updated', board);
    });
  }
}
