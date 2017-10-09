import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/mergeMap';
import { WriterService, Writer } from '../writer.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-writer',
  templateUrl: './writer.component.html',
  styleUrls: ['./writer.component.css']
})
export class WriterComponent implements OnInit {
  writerWritings$: Observable<string[]>;
  writerName$: Observable<string>;

  constructor(private activatedRoute: ActivatedRoute, private writerService: WriterService, private router: Router) { }

  ngOnInit() {
    const writer$ = this.activatedRoute.params
      .map(x => x.writerId)
      .mergeMap(id => this.writerService.getWriter(id));
    this.writerName$ = writer$.map(x => x != null ? x.name : '');
    this.writerWritings$ = writer$.map(x => x != null ? x.writings : []);
  }

  changed(writingId: string) {
    this.router.navigate([`writing/${writingId}`], {
      relativeTo: this.activatedRoute
    });
  }

}
