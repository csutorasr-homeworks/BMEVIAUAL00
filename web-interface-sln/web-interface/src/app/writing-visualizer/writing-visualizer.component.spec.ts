import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WritingVisualizerComponent } from './writing-visualizer.component';

describe('WritingVisualizerComponent', () => {
  let component: WritingVisualizerComponent;
  let fixture: ComponentFixture<WritingVisualizerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WritingVisualizerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WritingVisualizerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
