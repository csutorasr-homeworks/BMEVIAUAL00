import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/pairwise';
import 'rxjs/add/operator/share';
import 'rxjs/add/observable/combineLatest';

import { WriterService, Stroke } from '../writer.service';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Component({
  selector: 'app-writing',
  templateUrl: './writing.component.html',
  styleUrls: ['./writing.component.css']
})
export class WritingComponent implements OnInit {
  strokes$: Observable<Stroke[]>;
  text$: Observable<string>;
  writerId$: Observable<string>;
  zoomSubject: BehaviorSubject<number>;
  zoom$: Observable<number>;
  selectedSubject: BehaviorSubject<{
    [key: string]: string
  }>;

  constructor(private activatedRoute: ActivatedRoute, private writerService: WriterService, private router: Router) { }

  ngOnInit() {
    this.selectedSubject = new BehaviorSubject({});
    // setup zoom
    this.zoomSubject = new BehaviorSubject(0.1);
    this.zoom$ = this.zoomSubject.asObservable();
    // load writing
    const writing$ = this.activatedRoute.params
      .mergeMap(x => this.writerService.getWriting(x.writerId, x.writingId)).share();
    // set data for bindings
    this.writerId$ = writing$.map(x => x.writerId);
    this.text$ = writing$.map(x => x.text);
    this.strokes$ = Observable.combineLatest(writing$, this.selectedSubject.asObservable())
      .map(([writing, selected]) => {
        Object.keys(selected).forEach(i => {
          writing.strokes[i].color = selected[i];
        });
        return writing.strokes;
      });
  }

  changeZoom(zoom) {
    this.zoomSubject.next(zoom);
  }

  selected(index) {
    const newValue = this.selectedSubject.value;
    if (index in newValue) {
      delete newValue[index];
    } else {
      newValue[index] = 'red';
    }
    this.selectedSubject.next(newValue);
  }
}
