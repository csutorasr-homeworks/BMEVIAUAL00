import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WriterSelectorComponent } from './writer-selector.component';

describe('WriterSelectorComponent', () => {
  let component: WriterSelectorComponent;
  let fixture: ComponentFixture<WriterSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WriterSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WriterSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
