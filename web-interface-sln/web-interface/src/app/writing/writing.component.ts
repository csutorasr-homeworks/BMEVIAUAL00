import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import 'rxjs/add/operator/combineLatest';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/pairwise';
import 'rxjs/add/operator/share';
import 'rxjs/add/operator/take';
import { HotkeysService, Hotkey } from 'angular2-hotkeys';

import { WriterService, Stroke, Orientation } from '../writer.service';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-writing',
  templateUrl: './writing.component.html',
  styleUrls: ['./writing.component.css']
})
export class WritingComponent implements OnInit, OnDestroy {
  manualHandednessSubscription: Subscription;
  manualHandedness: string;
  nextLink$: Observable<string>;
  reloadSubject: BehaviorSubject<{}>;
  calculatedHandedness$: Observable<Orientation>;
  manualHandedness$: Observable<Orientation>;
  log$: Observable<string>;
  strokes$: Observable<Stroke[]>;
  text$: Observable<string>;
  writerId$: Observable<string>;
  zoomSubject: BehaviorSubject<number>;
  zoom$: Observable<number>;
  selectedSubject: BehaviorSubject<{ [key: string]: string }>;
  selected$: Observable<{ [key: string]: string; }>;
  @ViewChild('next') next: ElementRef;
  hotheys: Hotkey[] = [
    new Hotkey('r', (event) => {
      this.next.nativeElement.click();
      event.preventDefault();
      return false;
    }),
    new Hotkey('a', (event) => {
      this.changeManualHandedness('left');
      event.preventDefault();
      return false;
    }),
    new Hotkey('s', (event) => {
      this.changeManualHandedness('right');
      event.preventDefault();
      return false;
    }),
    new Hotkey('d', (event) => {
      this.changeManualHandedness('unknown');
      event.preventDefault();
      return false;
    })
  ];

  constructor(private activatedRoute: ActivatedRoute, private writerService: WriterService, private router: Router,
    private hotkeysService: HotkeysService) { }

  ngOnInit() {
    this.selectedSubject = new BehaviorSubject({});
    this.selected$ = this.selectedSubject.asObservable();
    // setup zoom
    this.zoomSubject = new BehaviorSubject(0.1);
    this.zoom$ = this.zoomSubject.asObservable();
    // load writing
    this.reloadSubject = new BehaviorSubject({});
    const writing$ = this.activatedRoute.params
      .do(() => this.changeSelected())
      .combineLatest(this.reloadSubject.asObservable())
      .mergeMap(([x]) => this.writerService.getWriting(x.writerId, x.writingId)).share();
    // set data for bindings
    this.writerId$ = writing$.map(x => x.writerId);
    this.text$ = writing$.map(x => x.text);
    this.log$ = writing$.map(x => x.algorithmLog);
    this.manualHandedness$ = writing$.map(x => x.manualHandedness);
    this.manualHandednessSubscription = this.manualHandedness$.subscribe(x => this.manualHandedness = x ? x : 'default');
    this.calculatedHandedness$ = writing$.map(x => x.calculatedHandedness);
    this.strokes$ = writing$.map(x => x.strokes);
    this.nextLink$ = this.writerService.getNext(this.writerId$, writing$.map(x => x.writingId));
    // set up hotkeys
    this.hotkeysService.add(this.hotheys);
  }
  ngOnDestroy(): void {
    this.hotkeysService.remove(this.hotheys);
    this.manualHandednessSubscription.unsubscribe();
  }

  changeZoom(zoom) {
    this.zoomSubject.next(zoom);
  }

  changeSelected(index?) {
    if (typeof index !== 'undefined') {
      // single select
      this.selectedSubject.next({
        [index]: 'red'
      });
    } else {
      this.selectedSubject.next({});
    }
  }

  changeSelectionType(type: Orientation | 'nohorizontal') {
    const subscription = this.activatedRoute.params.combineLatest(this.selected$)
      .take(1)
      .mergeMap(([params, selected]) => {
        if (Object.keys(selected).length === 0) {
          throw new Error('No selected stroke.');
        }
        const lineIndex = Object.keys(selected)[0];
        // Do the operation
        if (type === 'nohorizontal') {
          return this.writerService.removeHorizontalLine(params.writerId, params.writingId, +lineIndex);
        } else {
          return this.writerService.addHorizontalLine(params.writerId, params.writingId, +lineIndex, type);
        }
      }).subscribe(() => {
        this.reloadSubject.next({});
        this.changeSelected();
        subscription.unsubscribe();
      });
  }

  changeManualHandedness(type: Orientation) {
    const subscription = this.activatedRoute.params.mergeMap(params => {
      return this.writerService.changeManualHandedness(params.writerId, params.writingId, type);
    }).subscribe(x => {
      this.reloadSubject.next({});
      this.changeSelected();
      subscription.unsubscribe();
    });
  }

  selectClicked(event: Event) {
    event.stopPropagation();
  }
}
