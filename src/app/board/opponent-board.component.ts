import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { GameStateService, Board } from '../game-state.service';

/**
 * OpponentBoardComponent displays the opponent's board.
 * It only shows hit and miss markers, never ship positions.
 */
@Component({
  selector: 'app-opponent-board',
  templateUrl: './opponent-board.component.html',
  styleUrls: ['./opponent-board.component.scss']
})
export class OpponentBoardComponent implements OnInit {
  board$!: Observable<Board>;

  constructor(private gameState: GameStateService) {}

  ngOnInit(): void {
    this.board$ = this.gameState.opponentBoard$;
  }
}
