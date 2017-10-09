import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StrokeDataChangerComponent } from './stroke-data-changer.component';

describe('StrokeDataChangerComponent', () => {
  let component: StrokeDataChangerComponent;
  let fixture: ComponentFixture<StrokeDataChangerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StrokeDataChangerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StrokeDataChangerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
