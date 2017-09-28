import { Component, OnInit } from '@angular/core';
import { WriterService } from '../writer.service';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';

@Component({
  selector: 'app-writer-selector',
  templateUrl: './writer-selector.component.html',
  styleUrls: ['./writer-selector.component.css']
})
export class WriterSelectorComponent implements OnInit {
  writers$: Observable<string[]>;

  constructor(private writerService: WriterService, private router: Router) { }

  ngOnInit() {
    this.writers$ = this.writerService.getList();
  }

  changed(newValue: string) {
    if (newValue === 'null') {
      this.router.navigateByUrl('');
      return;
    }
    this.router.navigateByUrl('writer/' + newValue);
  }

}
