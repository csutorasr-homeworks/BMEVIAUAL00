import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import 'rxjs/add/operator/mergeMap';

import { WriterService } from '../writer.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-writing',
  templateUrl: './writing.component.html',
  styleUrls: ['./writing.component.css']
})
export class WritingComponent implements OnInit {
  text$: Observable<string>;
  writerId$: Observable<string>;

  constructor(private activatedRoute: ActivatedRoute, private writerService: WriterService, private router: Router) { }

  ngOnInit() {
    const writing$ = this.activatedRoute.params
      .mergeMap(x => this.writerService.getWriting(x.writerId, x.writingId)).do(x => console.log(x));
    this.writerId$ = writing$.map(x => x.writerId);
    this.text$ = writing$.map(x => x.text);
  }

}
