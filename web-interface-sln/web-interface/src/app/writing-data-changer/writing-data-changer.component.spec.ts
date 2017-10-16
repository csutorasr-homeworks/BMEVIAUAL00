import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WritingDataChangerComponent } from './writing-data-changer.component';

describe('WritingDataChangerComponent', () => {
  let component: WritingDataChangerComponent;
  let fixture: ComponentFixture<WritingDataChangerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WritingDataChangerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WritingDataChangerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
