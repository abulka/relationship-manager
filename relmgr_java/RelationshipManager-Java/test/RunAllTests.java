import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        FindCacheFullTest1.class,
        NewEmptyJUnitTest.class,
        UnitTest1.class,
        UnitTestBackLinks.class,
        UnitTestBidirectional.class,
        UnitTestBidirectional2.class,
        UnitTestCacheBug.class,
        UnitTestClearAndCount.class,
        UnitTestEnforcement.class,
        UnitTestEnforcementVisioExamples.class,
        UnitTestMiscQuerying.class,
        UnitTestNullSituations.class,
        UnitTestRMShortHand.class
        })
public class RunAllTests {
}