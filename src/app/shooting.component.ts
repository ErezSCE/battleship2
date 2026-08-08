import { Component, Input } from '@angular/core';
import { FireShotService } from './services/fire-shot.service';

@Component({
  selector: 'app-shooting',
  templateUrl: './shooting.component.html',
  styleUrls: ['./shooting.component.scss']
})
export class ShootingComponent {
  @Input() shooterId!: string;
  @Input() gameId!: string;
  x: number = 0;
  y: number = 0;
  result: string | null = null;

  constructor(private fireShotService: FireShotService) {}

  fire(): void {
    // Validate coordinates are within board bounds (0-9)
    if (this.x < 0 || this.x > 9 || this.y < 0 || this.y > 9) {
      this.result = 'Error: coordinates out of bounds';
      return;
    }
    if (!this.gameId) {
      console.error('gameId is required to fire a shot');
      return;
    }
    this.fireShotService.fireShot(this.gameId, this.shooterId, this.x, this.y).subscribe(
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
