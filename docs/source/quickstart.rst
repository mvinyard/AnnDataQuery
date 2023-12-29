===========
Quick Start
===========

.. role::  raw-html(raw)
    :format: html


Install & import the library
----------------------------

.. code-block:: shell

   pip install adata-query

.. code-block:: python

   import adata_query


AnnData
-------

This package is downstream of data loading and assumes a generally typical implementation of adata created using the AnnData package or Scanpy. 

.. code-block:: python

   import anndata

   h5ad_path = "/path/to/your/adata.h5ad"

   adata = anndata.read_h5ad(h5ad_path)


Once you have some data, you are ready to interface with ``adata_query``.

``adata_query.fetch``
---------------------

The ``fetch`` function is probably the most useful function in the library. It's also
the most function most likely to be touched by the user. It relies on the other two 
functions in the library: ``locate`` and ``format_data``. (described briefly, below). 

In short, this function finds a matrix stored in ``adata`` using ``str`` keyword.
Importantly, this function allows the user to do this in a grouped fashion, based
on ``pd.groupby``

.. tab-set::

   .. tab-item:: Ungrouped

      .. card:: Ungrouped

         .. code-block:: python

            key = "X_pca" # stored in adata.obsm

            data = adata_query.fetch(adata = adata, key = "X_pca")

   .. tab-item:: Grouped

      .. card:: Grouped
         
         .. code-block:: python

            key = "X_pca" # stored in adata.obsm
            groupby = "cluster" # cell annotation in adata.obs

            data = adata_query.fetch(
               adata = adata,
               key = key,
               groupby = groupby,
            )

         In this example, ``data`` is returned as ``List``.


``adata_query.format_data``
---------------------------
This function allows us to automatically format data stored as
``np.ndarray`` as a ``torch.Tensor``, on any device.

.. tab-set::

   .. tab-item:: numpy :raw-html:`&rarr;` numpy

      .. card:: numpy :raw-html:`&rarr;` numpy

         .. code-block:: python

            data = adata_query.format(data) # returns np.ndarray

   .. tab-item:: numpy :raw-html:`&rarr;` torch (cpu)

      .. card:: numpy :raw-html:`&rarr;` torch (cpu)
         
         .. code-block:: python
                        
            data = adata_query.format(data, torch = True, device = "cpu") # torch.Tensor on cpu
            

   .. tab-item:: numpy :raw-html:`&rarr;` torch (gpu)

      .. card:: numpy :raw-html:`&rarr;` torch (gpu)
         
         .. code-block:: python

            data = adata_query.format(data, torch = True) # torch.Tensor on gpu, if available

            # torch.Tensor can also be explicitly declared to a specific device
            data = adata_query.format(data, torch = True, device = "cuda:0")
            
            # Apple Silicon also works and will be automatically detected
            data = adata_query.format(data, torch = True, device = "mps:0")



``adata_query.locate``
----------------------
This function simply returns the sub-container location of a matrix,
given its accessor key. While useful in the implementation of the 
``adata_query.fetch`` function, it is not anticipated to be widely-used
beyond that scope.

.. card::
   .. code-block:: python

      import adata_query

      key = "X_pca"
      attr_key = adata_query.locate(adata, key = key) # attr_key = "obsm"


.. note::

   While both the ``format_data`` and ``locate`` functions may seem trivial,
   they are useful in adding flexibility to complex workflows.