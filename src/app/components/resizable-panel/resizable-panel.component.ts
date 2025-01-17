import { Component, effect, ElementRef, input, output, Renderer2, signal, ViewEncapsulation } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { AppButton } from '../../components/app-button/app-button.component';
import { MatTooltip } from '@angular/material/tooltip';

@Component({
  selector: 'resizable-panel',
  imports: [MatIconModule, AppButton, MatTooltip],
  templateUrl: './resizable-panel.component.html',
  styleUrl: './resizable-panel.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class ResizablePanel{

  width = input.required<string>();

  panelVisibility = input<boolean>(true)
  panelVisibilityIconClick = output<void>();

  constructor(private el: ElementRef, private renderer: Renderer2) {
    effect (() => {
      if (!this.panelVisibility()) {
        const currentWidth = this.el.nativeElement.getBoundingClientRect().width;
        this.renderer.setStyle(this.el.nativeElement, 'margin-left', `-${currentWidth}px`);
      } else {
        this.renderer.setStyle(this.el.nativeElement, 'margin-left', 0);
      }
    });
  }

  ngOnInit() {
    this.renderer.setStyle(this.el.nativeElement, 'width', this.width());
    this.renderer.setStyle(this.el.nativeElement, 'height', '100%');
    this.renderer.setStyle(this.el.nativeElement, 'transition', 'margin-left 1s');
  }
}
