import micromagneticmodel as mm


class System(mm.System):
    """Micromagnetic system oject.

    Parameters
    ----------
    name : str

    Examples
    --------
    Creating a simple system object.

    >>> import mumaxc as mc
    >>> system = mc.System(name="my_system")

    """
    @property
    def _script(self):
        mx3 = "mu0mm:={}\n\n".format(mm.mu0)
        mx3 += self.m.mesh._script
        mx3 += self.hamiltonian._script
        return mx3

    def total_energy(self):
        return self.dt.tail(1)["E"][0]

    def howtocite(self):
       bibs=[]
       for i in range(self.drive_number):
           dirname=f"{self.name}/drive-{i}/{self.name}.out/references.bib"
           with open(dirname) as f:
               bibs.append(f.read())
       bibs="".join(bibs)
       bibs=bibs.split("---------------------------------------------------------------------------")
       bibs=set(bibs)
       bibs=list(bibs)
       for j in range(1,len(bibs)-1):
           if "This bibtex file" in bibs[j]:
               bibs.remove(bibs[j])
          
       for j in range(1,len(bibs)):
           if "Main paper" in bibs[j]:
               mainpaper=bibs[j]
               bibs.remove(bibs[j])
               bibs.insert(1,mainpaper)
               

       joommfpaper="""
Ubermag interface

@article{Beg2017a,
    author = {Beg, Marijan and
              Pepper, Ryan A  and
              Fangohr, Hans},
    title = {{User interfaces for computational science: A domain specific language for OOMMF embedded in Python}},
    journal = {AIP Advances},
    number = {5},
    pages = {056025},
    volume = {7},
    year = {2017}
    doi = {10.1063/1.4977225},
    url = {http://aip.scitation.org/doi/10.1063/1.4977225},
}

"""
       bibs="".join(bibs)
       print(bibs)
       print(joommfpaper)
        
