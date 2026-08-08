import { Component, Input } from '@angular/core';
import { GameService } from './game.service';

@Component({
  selector: 'app-shooting',
  templateUrl: './shooting.component.html',
  styleUrls: ['./shooting.component.scss']
})
export class ShootingComponent {
  @Input() gameId!: string;
  x: number = 0;
  y: number = 0;
  result: string | null = null;

  constructor(private gameService: GameService) {}

  fire(): void {
    if (!this.gameId) {
      console.error('gameId is required to fire a shot');
      return;
    }
    this.gameService.fireShot(this.gameId, this.x, this.y).subscribe(
      (res) => {
        // Expect response to contain a result field like "hit", "miss", or "sunk"
        this.result = res?.result ?? JSON.stringify(res);
      },
      (err) => {
        this.result = `Error: ${err?.message || err}`;
      }
    );
  }
}
