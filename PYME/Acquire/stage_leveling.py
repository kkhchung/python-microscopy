
import numpy as np

class StageLeveler(object):
    def __init__(self, scope, offset_piezo):
        """
        Allows semi-automated mapping of coverslip positions are various lateral positions using a focus lock/offset
        piezo to determine the offset.

        Usage after initialization
        --------------------------
        1 Manually, e.g. with joystick, move the stage to various positions and call the `add_position` method at each.
        2 Run `measure_offsets` to automatically visit each of these positions and log the offset.
        3 Call `plot` to have a look at the map and get a feel for any adjustments you need to make on the hardware

        Parameters
        ----------
        scope: PYME.Acquire.microscope.microscope
        offset_piezo: PYME.Acquire.Hardware.offsetPiezoREST.OffsetPiezo

        Notes
        -----
        Units are derived from PYME.Acquire.microscope.microscope.GetPos and SetPos and should be in micrometers.

        """
        self._scope = scope
        self._offset_piezo = offset_piezo
        self._positions = []
        self._scans = []

    def clear_positions(self):
        self._positions = []

    def add_position(self):
        self._positions.append(self._scope.GetPos())

    def measure_offsets(self):
        """
        Visit each position and log the offset

        """
        n_positions = len(self._positions)
        x = np.zeros(len(self._positions), dtype=float)
        y = np.zeros_like(x)
        offset = np.zeros_like(x)

        for ind in range(n_positions):
            self._scope.SetPos(x=self._positions[ind]['x'], y=self._positions[ind]['y'])
            actual = self._scope.GetPos()
            x[ind], y[ind] = actual['x'], actual['y']
            offset[ind] = self._offset_piezo.GetOffset()

        self._scans.append({
            'x': x, 'y': y, 'offset': offset
        })

    @staticmethod
    def plot_scan(scan=None, interpolation_factor=50):
        """

        Parameters
        ----------
        scan: dict
            x: x positions
            y: y positions
            offset: offset positions
        interpolation_factor: int
            number of points along x and y to interpolate the offset map.

        """
        import matplotlib.pyplot as plt
        from scipy.interpolate import griddata

        x_min, x_max = np.min(scan['x']), np.max(scan['x'])
        y_min, y_max = np.min(scan['y']), np.max(scan['y'])

        x_grid, y_grid = np.meshgrid(np.linspace(x_min, x_max, interpolation_factor),
                                     np.linspace(y_min, y_max, interpolation_factor),
                                     indexing='ij')

        scan_map = griddata(np.stack([scan['x'], scan['y']]), scan['offset'], np.stack((x_grid, y_grid)))

        plt.figure()
        plt.imshow(scan_map, interpolation='nearest')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Offset [um]')
        plt.scatter(scan['x'], scan['y'], marker='x', label='measured')
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot(self, index=-1, interpolation_factor=50):
        if len(self._scans) < 1:
            raise UserWarning('no scans available, call StageLeveler.measure_offsets() first')
        StageLeveler.plot_scan(self._scans[index], interpolation_factor=interpolation_factor)
