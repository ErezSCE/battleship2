import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ShipPlacementComponent } from './ship-placement.component';
import { By } from '@angular/platform-browser';

describe('ShipPlacementComponent', () => {
  let component: ShipPlacementComponent;
  let fixture: ComponentFixture<ShipPlacementComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ShipPlacementComponent],
      imports: [HttpClientTestingModule]
    }).compileComponents();

    fixture = TestBed.createComponent(ShipPlacementComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should select a ship', () => {
    component.selectShip(0);
    expect(component.selectedShipIndex).toBe(0);
    // selecting already placed ship should not change selection
    component.shipsToPlace[0].placed = true;
    component.selectShip(0);
    expect(component.selectedShipIndex).toBe(0); // remains previous selection
  });

  it('should toggle orientation of selected ship', () => {
    component.selectShip(1);
    const ship = component.shipsToPlace[1];
    const initial = ship.orientation;
    component.toggleOrientation();
    expect(ship.orientation).not.toBe(initial);
    component.toggleOrientation();
    expect(ship.orientation).toBe(initial);
  });

  it('should accept a valid placement and mark ship as placed', () => {
    component.selectShip(0); // size 2, horizontal
    component.onCellClick(0, 0);
    expect(component.placements.length).toBe(1);
    expect(component.shipsToPlace[0].placed).toBeTrue();
    expect(component.selectedShipIndex).toBe(-1);
  });

  it('should reject out-of-bounds placement', () => {
    component.selectShip(0); // size 2 horizontal
    component.onCellClick(5, 5); // would exceed board horizontally
    expect(component.placements.length).toBe(0);
    expect(component.shipsToPlace[0].placed).toBeFalse();
  });

  it('should reject overlapping placement', () => {
    // place first ship at (0,0) size 2 horizontal
    component.selectShip(0);
    component.onCellClick(0, 0);
    // attempt second ship overlapping first
    component.selectShip(1); // size 3 horizontal
    component.onCellClick(0, 0);
    expect(component.placements.length).toBe(1); // second not added
    expect(component.shipsToPlace[1].placed).toBeFalse();
  });

  it('should submit placements with correct payload', () => {
    // place all three ships validly
    // ship 0 size2 horizontal at (0,0)
    component.selectShip(0);
    component.onCellClick(0, 0);
    // ship 1 size3 vertical at (2,0)
    component.selectShip(1);
    component.toggleOrientation(); // now vertical
    component.onCellClick(2, 0);
    // ship 2 size4 horizontal at (0,2)
    component.selectShip(2);
    component.onCellClick(0, 2);

    expect(component.placements.length).toBe(3);

    component.submitPlacements().subscribe();
    const req = httpMock.expectOne(`/games/${component.gameId}/ships`);
    expect(req.request.method).toBe('POST');
    const expectedPayload = component.placements.map(p => ({
      size: p.size,
      orientation: p.orientation,
      start_x: p.startX,
      start_y: p.startY
    }));
    expect(req.request.body).toEqual(expectedPayload);
    req.flush({}); // respond with empty body
  });
});
