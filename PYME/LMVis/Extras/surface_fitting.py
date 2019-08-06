
import numpy as np

class SurfaceFitter(object):
    def __init__(self, vis_frame):
        self.vis_frame = vis_frame

        self.vis_frame.AddMenuItem('Analysis>Surface Fitting', "Fit Surface With Quadratic Patches",
                                   self.OnFitQuadraticPatches)
        
    
    def OnFitQuadraticPatches(self, event):
        """

        Parameters
        ----------
        event: wx.Event

        Returns
        -------

        """
        from PYME.recipes.surface_fitting import SurfacePatchFitter
        pipeline = self.vis_frame.pipeline
        # hold off auto-running the recipe until we configure things
        pipeline.recipe.trait_set(execute_on_invalidation=False)

        raw_key = 'quadratic_surface_fits_raw'
        filtered_key = 'quadratic_surface_fits_filtered'
        reconstruction_key = 'quadratic_surface'
        try:
            fit_module = SurfacePatchFitter(pipeline.recipe, input=pipeline.selectedDataSourceKey,
                                            out_fits_raw=raw_key, out_fits_filtered=filtered_key,
                                            out_surface_reconstruction=reconstruction_key)

            pipeline.recipe.add_module(fit_module)
            if not pipeline.recipe.configure_traits(view=pipeline.recipe.pipeline_view, kind='modal'):
                return

            pipeline.recipe.execute()
            pipeline.addDataSource(raw_key, pipeline.recipe.namespace[raw_key], False)
            pipeline.addDataSource(filtered_key, pipeline.recipe.namespace[filtered_key], False)
            pipeline.addDataSource(reconstruction_key, pipeline.recipe.namespace[reconstruction_key], False)

        finally:  # make sure that we configure the pipeline recipe as it was
            pipeline.recipe.trait_set(execute_on_invalidation=True)

        # refresh our view
        pipeline.selectDataSource(reconstruction_key)
        pipeline.Rebuild()
        
        self.vis_frame.Refresh()


def Plug(visFr):
    '''Plugs this module into the gui'''
    SurfaceFitter(visFr)