import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {SidenavType} from 'mesop/mesop/components/sidenav/sidenav_jspb_proto_pb/mesop/components/sidenav/sidenav_pb';
import {Channel} from '../../web/src/services/channel';
import {MatSidenavModule} from '@angular/material/sidenav';

@Component({
  selector: 'mesop-sidenav',
  templateUrl: 'sidenav.ng.html',
  standalone: true,
  imports: [MatSidenavModule],
})
export class SidenavComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: SidenavType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = SidenavType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): SidenavType {
    return this._config;
  }
}
