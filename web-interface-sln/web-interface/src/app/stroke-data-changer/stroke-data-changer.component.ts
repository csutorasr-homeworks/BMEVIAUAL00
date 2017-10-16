import { Component, OnInit, Input, EventEmitter, Output, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormControl } from '@angular/forms';
import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/combineLatest';

import { Stroke } from '../writer.service';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-stroke-data-changer',
  templateUrl: './stroke-data-changer.component.html',
  styleUrls: ['./stroke-data-changer.component.css']
})
export class StrokeDataChangerComponent implements OnInit, OnDestroy {
  valueSubscription: Subscription;
  isSelected$: Observable<boolean>;
  @Input() selected$: Observable<{ [key: string]: string; }>;
  @Input() strokes$: Observable<Stroke[]>;
  @Output() changeType = new EventEmitter();

  select = new FormControl();

  constructor() { }

  ngOnInit() {
    this.isSelected$ = this.selected$.map(x => Object.keys(x).length !== 0);
    const strokeIndex$ = this.selected$.map(x => Object.keys(x))
      .filter(x => x.length !== 0)
      .map(x => x[0]);
    const stroke$: Observable<Stroke> = strokeIndex$.combineLatest(this.strokes$).map(([index, strokes]) => strokes[index]);
    this.valueSubscription = stroke$.map(x => x.strokeDirection).subscribe(x => {
      if (x) {
        this.select.patchValue(x);
      } else {
        this.select.patchValue('nohorizontal');
      }
    });
  }

  ngOnDestroy(): void {
    this.valueSubscription.unsubscribe();
  }

  valueChanged() {
    this.changeType.emit(this.select.value);
  }
}
