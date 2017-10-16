import { Component, OnInit, Input, OnDestroy, Output, EventEmitter } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormControl } from '@angular/forms';
import { Subscription } from 'rxjs/Subscription';
import { Orientation } from '../writer.service';

@Component({
  selector: 'app-writing-data-changer',
  templateUrl: './writing-data-changer.component.html',
  styleUrls: ['./writing-data-changer.component.css']
})
export class WritingDataChangerComponent implements OnInit, OnDestroy {
  subscription: Subscription;
  @Input() text$: Observable<string>;
  @Input() log$: Observable<string>;
  @Input() manualHandedness$: Observable<Orientation>;
  @Input() calculatedHandedness$: Observable<Orientation>;
  @Output() changeManualHandedness = new EventEmitter();
  manualHandedness = new FormControl();

  constructor() { }

  ngOnInit() {
    this.subscription = this.manualHandedness$.subscribe(x => {
      if (x) {
        this.manualHandedness.patchValue(x);
      } else {
        this.manualHandedness.patchValue('default');
      }
    });
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  manualHandednessChanged() {
    this.changeManualHandedness.next(this.manualHandedness.value);
  }
}
