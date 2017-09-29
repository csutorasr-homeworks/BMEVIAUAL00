import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/pairwise';
import 'rxjs/add/operator/share';
import 'rxjs/add/observable/of';

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

  constructor(private activatedRoute: ActivatedRoute, private writerService: WriterService, private router: Router) { }

  ngOnInit() {
    this.zoomSubject = new BehaviorSubject(0.1);
    this.zoom$ = this.zoomSubject.asObservable();
    const writing$ = this.activatedRoute.params
      .mergeMap(x => this.writerService.getWriting(x.writerId, x.writingId)).share();
    this.writerId$ = writing$.map(x => x.writerId);
    this.text$ = writing$.map(x => x.text);
    this.strokes$ = writing$.map(x => x.strokes);
  }

  changeZoom(zoom) {
    this.zoomSubject.next(zoom);
  }

  selected(index) {
    alert(index);
  }
}
