import { Component, OnInit, Output, EventEmitter, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-zoom',
  templateUrl: './zoom.component.html',
  styleUrls: ['./zoom.component.css']
})
export class ZoomComponent implements OnInit, OnDestroy {
  subscription: Subscription;
  @Output() zoom$ = new EventEmitter<number>();
  zoomSubject: BehaviorSubject<number>;

  constructor() { }

  ngOnInit() {
    this.zoomSubject = new BehaviorSubject(0.1);
    this.subscription = this.zoomSubject.subscribe(x => this.zoom$.next(x));
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  zoomIn() {
    this.zoomSubject.next(this.zoomSubject.value * 2);
  }

  zoomOut() {
    this.zoomSubject.next(this.zoomSubject.value * 0.5);
  }

}
