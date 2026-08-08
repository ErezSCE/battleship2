import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FireShotService } from './fire-shot.service';

describe('FireShotService', () => {
  let service: FireShotService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [FireShotService]
    });
    service = TestBed.inject(FireShotService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should POST shot coordinates to the correct endpoint and return response', () => {
    const mockResponse = { result: 'hit', turn: 'player2' };
    const gameId = 'game123';
    const x = 3;
    const y = 5;

    service.fireShot(gameId, x, y).subscribe((res) => {
      expect(res).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`/games/${gameId}/shots`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ x, y });
    req.flush(mockResponse);
  });
});
