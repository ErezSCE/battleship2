import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BoardComponent } from './board.component';
import { GameStateService } from '../game-state.service';
import { By } from '@angular/platform-browser';
import { of } from 'rxjs';

describe('BoardComponent', () => {
  let component: BoardComponent;
  let fixture: ComponentFixture<BoardComponent>;
  let mockService: Partial<GameStateService>;

  const emptyBoard = Array.from({ length: 10 }, () =>
    Array.from({ length: 10 }, () => 'empty' as const)
  );

  beforeEach(async () => {
    mockService = {
      playerBoard$: of(emptyBoard)
    } as Partial<GameStateService>;

    await TestBed.configureTestingModule({
      declarations: [BoardComponent],
      providers: [{ provide: GameStateService, useValue: mockService }]
    }).compileComponents();

    fixture = TestBed.createComponent(BoardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render a 10x10 grid of empty cells', () => {
    const cellElements = fixture.debugElement.queryAll(By.css('.cell'));
    expect(cellElements.length).toBe(100);
    // All cells should have class 'empty'
    cellElements.forEach(el => {
      expect(el.nativeElement.classList).toContain('empty');
    });
  });
});
