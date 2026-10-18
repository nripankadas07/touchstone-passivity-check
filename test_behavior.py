import unittest,math
from touchstone_passivity_check import analyze
H='# GHz S RI R 50\n'
class NetworkTests(unittest.TestCase):
 def test_lossless_through(self):
  r=analyze(H+'1 0 0 1 0 1 0 0 0',2);self.assertEqual(r['samples'][0]['max_singular_value'],1);self.assertFalse(r['failing_sample_indices'])
 def test_coupled_gain_not_detectable_from_columns_alone(self):
  r=analyze(H+'1 .7 0 .7 0 .7 0 .7 0',2);self.assertAlmostEqual(r['samples'][0]['max_singular_value'],1.4);self.assertEqual(r['failing_sample_indices'],[0])
 def test_one_port(self):self.assertEqual(analyze(H+'1 .3 .4',1)['samples'][0]['max_singular_value'],.5)
 def test_identity(self):self.assertEqual(analyze(H+'1 1 0 0 0 0 0 1 0',2)['samples'][0]['largest_power_gain'],1)
 def test_ma_and_db_equivalence(self):
  a=analyze('# MHz S MA R 75\n1000 .5 90',1);b=analyze('# GHz S DB R 75\n1 -6.020599913279624 90',1);self.assertAlmostEqual(a['samples'][0]['largest_power_gain'],b['samples'][0]['largest_power_gain']);self.assertEqual(a['shared_real_reference_ohms'],75)
 def test_nonreciprocal_can_be_passive(self):
  r=analyze(H+'1 0 0 .5 0 0 0 0 0',2);self.assertFalse(r['failing_sample_indices']);self.assertEqual(r['samples'][0]['reciprocity_difference'],.5)
 def test_continuations(self):self.assertEqual(analyze(H+'1\n0 0 1 0\n1 0 0 0',2)['samples'][0]['frequency_hz'],1e9)
 def test_zero_frequency(self):self.assertEqual(analyze(H+'0 0 0',1)['samples'][0]['frequency_hz'],0)
 def test_comments(self):self.assertEqual(analyze('! invented\n'+H+'1 0 0 ! x',1)['ignored_comments'],2)
 def test_tolerance(self):
  self.assertFalse(analyze(H+'1 1.0000001 0',1,1e-6)['failing_sample_indices']);self.assertTrue(analyze(H+'1 1.0000001 0',1,0)['failing_sample_indices'])
 def test_frequency_order(self):
  for x in ['1 0 0 1 0 0','2 0 0 1 0 0','-1 0 0']:
   with self.assertRaises(ValueError):analyze(H+x,1)
 def test_incomplete_and_options(self):
  for x in ['1 0 0',H+'1 0',H+'# GHz S RI R 50\n1 0 0',H.replace(' S ',' Z ')+'1 0 0',H.replace('R 50','R -1')+'1 0 0']:
   with self.assertRaises(ValueError):analyze(x,1)
 def test_unsupported_extensions(self):
  for x in [H+'[Version] 2.0',H+'1 0 0 ! Port Impedance 50 0']:
   with self.assertRaises(ValueError):analyze(x,1)
 def test_nonfinite_and_numeric_budgets(self):
  for x in ['1 nan 0','1 1e999 0','1 1001 0']:
   with self.assertRaises(ValueError):analyze(H+x,1)
 def test_reference_and_tolerance_bounds(self):
  for t in [-1,float('nan'),.01]:
   with self.assertRaises(ValueError):analyze(H+'1 0 0',1,t)
 def test_size_and_sample_budgets(self):
  with self.assertRaises(ValueError):analyze(' '*(1024*1024+1),1)
  with self.assertRaises(ValueError):analyze(H+'0 0 0\n'*4097,1)
if __name__=='__main__':unittest.main()
